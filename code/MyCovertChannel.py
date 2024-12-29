from scapy.all import ARP, sniff, Ether
from time import time, sleep
from CovertChannelBase import CovertChannelBase

class MyCovertChannel(CovertChannelBase):
    """
    Implementation of a covert channel exploiting packet inter-arrival times using ARP packets.
    """

    def __init__(self):
        super().__init__()

    def send(self, log_file_name, send_0_wait, send_1_wait):
        """
        Send a random covert message using ARP packets and inter-packet timing. Send a stopping signal
        at the end and wait a small amount to ensure the receiver has received the message.

        Args:
            log_file_name (str): Name of the log file to record the sent message.
            send_0_wait: Time (in milliseconds) to wait between packets to send bit 0
            send_1_wait: Time (in milliseconds) to wait between packets to send bit 1
        """
       
        binary_message = self.generate_random_binary_message_with_logging(str(log_file_name))

        for bit in binary_message:
            packet = Ether(dst = "ff:ff:ff:ff:ff:ff") / ARP(pdst="172.18.0.3") 

            super().send(packet)

            if bit == "0":
                sleep(send_0_wait)  # for 0
            else:
                sleep(send_1_wait)  # for 1

        super().send(Ether(dst = "ff:ff:ff:ff:ff:ff") / ARP(pdst="172.18.0.3"))
        sleep(0.2)

    def receive(self, log_file_name, upper_boundary_0, upper_boundary_1):
        """
        Receive and decode the covert message from ARP packets (1 packet at a time). 
        Deduce the bit value from the wait time between packets and check for the end of message 
        at each byte received.

        Args:
            log_file_name (str): Name of the log file to record the received message.
            upper_boundary_0: The upper boundary of wait time (in milliseconds) to interpret the bit as 0.
            upper_boundary_1: The upper boundary of wait time (in milliseconds) to interpret the bit as 1.
        """
        received_message = ""

        packet_list = sniff(filter="arp", iface="eth0", count=1)
        last_time = time()
        while True:
            packet_list = sniff(filter="arp", iface="eth0", count=1)
            current_time = time()
            inter_arrival_time = current_time - last_time
            last_time = current_time

            if inter_arrival_time < upper_boundary_0:
                received_message += "0"
            elif inter_arrival_time < upper_boundary_1:
                received_message += "1"
            else:
                # Stop on long delay (end of message)
                print("Long delay\n")
                break

            if len(received_message) % 8 == 0:
                byte = received_message[-8:]
                char = self.convert_eight_bits_to_character(byte)

                if char == ".": # Stop character received
                    break
        
        decoded_message = "".join(
            self.convert_eight_bits_to_character(received_message[i:i+8]) 
            for i in range(0, len(received_message), 8)
        )
        self.log_message(decoded_message, str(log_file_name))

