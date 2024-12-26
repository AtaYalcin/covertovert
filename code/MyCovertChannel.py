from CovertChannelBase import CovertChannelBase
from scapy.all import IP, UDP, Raw, send, sniff
import random

SENDER_IP = "172.18.0.2"
RECEIVER_IP = "172.18.0.3"

class MyCovertChannel(CovertChannelBase):
    def __init__(self):
        super().__init__()
        self.received_bits = ""
        self.received_messages = ""
        self.stop_event = False

    def send(self, log_file_name, min_size, max_size, threshold):
        """
        Encodes and sends the covert message using UDP packet size variation.

        - min_size: Minimum packet size
        - max_size: Maximum packet size
        - threshold: Size threshold to differentiate between 0 and 1
        """
        binary_message = self.generate_random_binary_message_with_logging(log_file_name)

        for bit in binary_message:
            if bit == '0':
                size = random.randint(min_size, threshold - 1)
            elif bit == '1':
                size = random.randint(threshold, max_size)
            else:
                raise "ERROR"

            payload = Raw(b'X' * size )  # 28 bytes for IP and UDP headers
            packet = IP(dst=RECEIVER_IP) / UDP(dport=12345, sport=12345) / payload
            super().send(packet)

        # Send termination packet
        #term_packet = IP(dst=RECEIVER_IP) / UDP(dport=12345, sport=12345) / Raw(b'.')
        #super().send(term_packet)

    def receive(self, log_file_name, min_size, max_size, threshold):
        """
        Receives and decodes the covert message from UDP packet size variation.

        - min_size: Minimum packet size
        - max_size: Maximum packet size
        - threshold: Size threshold to differentiate between 0 and 1
        """
        def process_packet(packet):
            if IP in packet and UDP in packet and packet[IP].src == SENDER_IP:
                payload = bytes(packet[Raw]) if Raw in packet else b''
                """
                if payload == b'.':
                    self.log_message(self.received_message, log_file_name)
                    self.stop_event = True
                    return
                """
                
                payload_size = len(payload)
                if min_size <= payload_size <= max_size:
                    bit = '1' if payload_size >= threshold else '0'
                    self.received_bits += bit

                    if len(self.received_bits) % 8 == 0:
                        
                        char = self.convert_eight_bits_to_character(self.received_bits[-8:])
                        #print(char)
                        self.received_messages += char
                        if char == '.':                            
                            self.log_message(self.received_messages, log_file_name)
                            self.stop_event = True

        sniff(filter="udp and port 12345", prn=process_packet, stop_filter=lambda _: self.stop_event)

    def stop_filter(self, packet):
        return self.stop_event
