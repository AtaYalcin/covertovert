from CovertChannelBase import CovertChannelBase
from scapy.all import IP, UDP, Raw, sniff
import random
import time

class MyCovertChannel(CovertChannelBase):
    SENDER_IP = "172.18.0.2"
    RECEIVER_IP = "172.18.0.3"
    UDP_PORT = 12345

    def __init__(self):
        super().__init__()
        self.received_bits = ""
        self.received_messages = ""
        self.stop_event = False

    def send(self, log_file_name, min_size, max_size, threshold):
        #Encodes and sends the covert message using UDP packet size variation.
        
        # Generate a random binary message and log it
        binary_message = self.generate_random_binary_message_with_logging(log_file_name)

        # Start timing for capacity calculation
        time_start = time.time()

        # Iterate through each bit in the message
        for bit in binary_message:
            # Determine payload size based on the bit value
            size = self._get_payload_size(bit, min_size, max_size, threshold)
            # Create a packet with the determined size
            packet = self._create_packet(size)
            # Send the packet using the parent class method
            super().send(packet)

        # End timing and calculate capacity
        time_end = time.time()
        capacity = len(binary_message) / (time_end - time_start)
        #print(f"Covert channel capacity: {capacity:.2f} bits per second")

    def receive(self, log_file_name, min_size, max_size, threshold):
        # Define a function to process each captured packet
        def packet_processor(pkt):
            return self._process_packet(pkt, log_file_name, min_size, max_size, threshold)
        
        # Define a function to check if sniffing should stop
        def stop_condition(_):
            return self.stop_event
    
        # Start sniffing packets with the defined processor and stop condition
        sniff(filter=f"udp and port {self.UDP_PORT}", 
              prn=packet_processor,
              stop_filter=stop_condition)

    def _get_payload_size(self, bit, min_size, max_size, threshold):
        # Determine payload size based on the bit value
        if bit == '0':
            return random.randint(min_size, threshold - 1)
        elif bit == '1':
            return random.randint(threshold, max_size)
        else:
            raise ValueError("Invalid bit value")

    def _create_packet(self, payload_size):
        # Create a UDP packet with the specified payload size
        payload = Raw(b'X' * payload_size)
        return IP(dst=self.RECEIVER_IP) / UDP(dport=self.UDP_PORT, sport=self.UDP_PORT) / payload

    def _process_packet(self, packet, log_file_name, min_size, max_size, threshold):
        # Check if the packet is a UDP packet from the sender
        if IP in packet and UDP in packet and packet[IP].src == self.SENDER_IP:
            payload = bytes(packet[Raw]) if Raw in packet else b''
            payload_size = len(payload)

            # If the payload size is within the expected range
            if min_size <= payload_size <= max_size:
                # Decode the bit based on the payload size
                bit = '1' if payload_size >= threshold else '0'
                self.received_bits += bit

                # If we have received 8 bits, convert them to a character
                if len(self.received_bits) % 8 == 0:
                    char = self.convert_eight_bits_to_character(self.received_bits[-8:])
                    self.received_messages += char
                    # If the character is a dot, log the message and stop receiving
                    if char == '.':
                        self.log_message(self.received_messages, log_file_name)
                        self.stop_event = True
