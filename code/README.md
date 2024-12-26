# Covert Storage Channel that exploits Packet Size Variation using UDP [Code: CSC-PSV-UDP]

## Capacity: 38.21 bits per second

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

# Performance
## Capacity
The covert channel capacity is calculated and printed after the transmission is complete. The exact capacity will depend on the network conditions and the chosen parameters (min_size, max_size, threshold). In our tests, we achieved a transmission rate of approximately X bits per second (replace X with your actual measured rate).


# Parameters
Our implementation uses the following parameters:

min_size: The minimum payload size for a packet.

max_size: The maximum payload size for a packet.

threshold: The size threshold to differentiate between '0' and '1' bits.

These parameters can be adjusted in the config.json file to optimize the channel's performance and stealth.

