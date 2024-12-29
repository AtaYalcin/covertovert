# Covert Storage Channel that exploits Packet Size Variation using UDP [Code: CSC-PSV-UDP]

## Capacity: 48.60 bits per second

# Implementation
Our covert channel implementation uses UDP packet size variation to encode and transmit data covertly. This method falls under the category of covert storage channels.

## Sender
The sender encodes the binary message by manipulating the size of UDP packets:

For each bit in the binary message:
If the bit is '0', the payload size is randomly chosen between min_size and threshold - 1.
If the bit is '1', the payload size is randomly chosen between threshold and max_size.
The sender creates UDP packets with the determined payload size and sends them to the receiver. The actual content of the payload is not important; it's filled with 'X' characters to achieve the desired packet size.

## Receiver
The receiver listens for incoming UDP packets and decodes the binary data by analyzing the packet size:

For each received packet:
If the payload size is less than threshold, it's decoded as '0'.
If the payload size is greater than or equal to threshold, it's decoded as '1'.
The receiver reconstructs the message by grouping 8 bits into a byte and converting it to a character. The transmission stops when a dot ('.') character is received.

# Parameters

The following parameters are used in the send function to optimize performance and stealth:

*log_file_name:* The name of the log file where messages will be recorded.

*min_size:* Minimum payload size for a packet.

*max_size:* Maximum payload size for a packet.

*threshold:* Size threshold to differentiate between '0' and '1' bits.

*SENDER_IP:* IP address of the sender.

*RECEIVER_IP:* IP address of the receiver.

*UDP_PORT:* Port number used for sending and receiving UDP packets.