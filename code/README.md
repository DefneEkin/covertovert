# Covert Timing Channel that exploits Packet Inter-Arrival Times using ARP 

This implementation is designed to create a covert timing channel using packet inter-arrival times. The implementation builds upon the CovertChannelBase class and employs ARP packets for transmitting a covert binary message.

Class Overview
The MyCovertChannel class leverages a covert timing channel, where data is encoded in the time intervals between packet transmissions. Two primary methods (send and receive) allow for sending and decoding a message.

Sender

Encode a random binary message into timing delays between ARP packets.
Transmit the encoded message to a receiver.
How it Works:

A random binary message is generated using a base class function, and the message is logged to a specified file.
For each bit in the binary message:
An ARP packet (Ethernet broadcast with a fixed destination IP) is sent.
A delay follows the packet. The delay duration (send_0_wait for "0" and send_1_wait for "1") encodes the binary data.
A final ARP packet signals the end of the message, followed by a short wait.
Parameters:

log_file_name: Logs the binary message for validation.
send_0_wait: Delay in milliseconds to represent bit "0".
send_1_wait: Delay in milliseconds to represent bit "1".
Limitations:

Network Delay: Real-world network delays could introduce variability in timing, affecting decoding accuracy.
Timing Resolution: The system clock’s resolution limits precision for very short delays.
Buffering: Network buffers could affect the packet timing observed by the receiver.
Receiving a Message: receive
Purpose:

Decode the binary message by analyzing packet inter-arrival times.
Interpret these delays to recreate the sent binary message.
How it Works:

ARP packets are captured using the sniff function, and the time between arrivals is calculated.
Thresholds (upper_boundary_0 and upper_boundary_1) categorize the delay as either bit "0", bit "1", or the end of the message.
Decoded bits are collected into an 8-bit chunk to form characters, which are printed when complete. The message ends upon receiving a stop character (.).
Parameters:

log_file_name: Logs the decoded message for validation.
upper_boundary_0: Maximum delay (in milliseconds) for interpreting a "0".
upper_boundary_1: Maximum delay (in milliseconds) for interpreting a "1".
Limitations:

Threshold Calibration: Upper boundaries must be tuned to the system and environment to account for variability in delays.
Packet Loss: Any missed packet could desynchronize decoding.
Noise in Timing: Non-covert traffic could affect measured timings.
Covert Channel Capacity
The capacity, in bits per second, is calculated by dividing the total bits (128 in this example) by the transmission time.
A faster decoding process and minimal network delays improve capacity, while noisy environments reduce it.
Logging and Debugging
Sent and received messages are logged for validation and debugging.
To analyze live traffic, tools like TShark can be used, as recommended in the instructions.
Practical Notes
Docker Environment: Ensure the code runs in the provided container environment to avoid compatibility issues.
Parameters in config.json: All delay thresholds and log filenames must be added to the configuration file for automated testing.
This implementation creatively utilizes inter-arrival timings, adhering to the constraints and objectives of covert channel communication. Proper parameter tuning and environment control are crucial for achieving reliable and high-capacity communication.
