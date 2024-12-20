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
        Send a covert message using ARP packets and inter-packet timing.

        Args:
            log_file_name (str): Name of the log file to record the sent message.
            parameter1: Placeholder parameter.
            parameter2: Placeholder parameter.
        """
        # Generate a binary message to send
        binary_message = self.generate_random_binary_message_with_logging(str(log_file_name))

        for bit in binary_message:
            # Create an ARP packet
            packet = Ether(dst = "ff:ff:ff:ff:ff:ff") / ARP(pdst="172.18.0.3") 

            # Send the packet
            super().send(packet)

            # Sleep based on the bit value
            if bit == "0":
                sleep(send_0_wait)  # for 0
            else:
                sleep(send_1_wait)  # for 1

        # Send a stopping signal (special packet)
        super().send(Ether(dst = "ff:ff:ff:ff:ff:ff") / ARP(pdst="172.18.0.3"))
        sleep(0.2)  # Ensure the receiver identifies the end of the message

    def receive(self, log_file_name, upper_boundary_0, upper_boundary_1):
        """
        Receive and decode the covert message from ARP packets.

        Args:
            parameter1: Placeholder parameter.
            parameter2: Placeholder parameter.
            parameter3: Placeholder parameter.
            log_file_name (str): Name of the log file to record the received message.
        """
        received_message = ""

        packet_list = sniff(filter="arp", iface="eth0", count=1)
        last_time = time()
        print("ilk mesaj geldi")
        while True:
            packet_list = sniff(filter="arp", iface="eth0", count=1)
            packet = packet_list[0]
            current_time = time()
            inter_arrival_time = current_time - last_time
            last_time = current_time

            if inter_arrival_time < upper_boundary_0:  # Less than 50 ms = 0
                received_message += "0"
            elif inter_arrival_time < upper_boundary_1:  # Between 50-150 ms = 1
                received_message += "1"
            else:
                # Stop on long delay (end of message)
                print("Long delay\n")
                break

            if len(received_message) % 8 == 0:
                byte = received_message[-8:]
                char = self.convert_eight_bits_to_character(byte)

                print(char)

                if char == ".":
                    # Stop character received
                    print("Stop character received\n")
                    break
        
        decoded_message = "".join(
            self.convert_eight_bits_to_character(received_message[i:i+8]) 
            for i in range(0, len(received_message), 8)
        )
        self.log_message(decoded_message, str(log_file_name))


            

     


'''
from CovertChannelBase import CovertChannelBase

class MyCovertChannel(CovertChannelBase):
    """
    - You are not allowed to change the file name and class name.
    - You can edit the class in any way you want (e.g. adding helper functions); however, there must be a "send" and a "receive" function, the covert channel will be triggered by calling these functions.
    """
    def __init__(self):
        """
        - You can edit __init__.
        """
        pass
    def send(self, log_file_name, parameter1, parameter2):
        """
        - In this function, you expected to create a random message (using function/s in CovertChannelBase), and send it to the receiver container. Entire sending operations should be handled in this function.
        - After the implementation, please rewrite this comment part to explain your code basically.
        """
        binary_message = self.generate_random_binary_message_with_logging(log_file_name)
        
    def receive(self, parameter1, parameter2, parameter3, log_file_name):
        """
        - In this function, you are expected to receive and decode the transferred message. Because there are many types of covert channels, the receiver implementation depends on the chosen covert channel type, and you may not need to use the functions in CovertChannelBase.
        - After the implementation, please rewrite this comment part to explain your code basically.
        """
        self.log_message("", log_file_name)
'''
