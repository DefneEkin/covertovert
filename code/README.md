# Covert Timing Channel that exploits Packet Inter-Arrival Times using ARP 

This project implements a covert timing channel using packet inter-arrival times. It builds on the `CovertChannelBase` class and leverages ARP packets to transmit a covert binary message. The following sections explain the implementation in detail.

---

## Class Overview
The `MyCovertChannel` class leverages a covert timing channel, where data is encoded in the time intervals between packet transmissions. Two primary methods (`send` and `receive`) allow for sending and decoding a message.

---

## `send`

### Purpose
- Encode a random binary message into timing delays between ARP packets.
- Transmit the encoded message to a receiver.

### How it Works
- A random binary message is generated using a base class function, and the message is logged to a specified file provided in `config.json`.
- For each bit in the binary message:
  - An ARP packet (Ethernet broadcast with a fixed destination IP) is sent.
  - A delay follows the packet. The delay duration (`send_0_wait` for "0" and `send_1_wait` for "1") encodes the binary data.
- A final ARP packet signals the end of the message, followed by a short wait.

### Parameters
- `log_file_name`: Logs the binary message for validation.
- `send_0_wait`: Delay in milliseconds to represent bit "0".
- `send_1_wait`: Delay in milliseconds to represent bit "1".

---

## `receive`

### Purpose
- Decode the binary message by analyzing packet inter-arrival times.
- Interpret these delays to recreate the sent binary message.

### How it Works
- ARP packets are captured using the `sniff` function, and the time between arrivals is calculated.
- Thresholds (`upper_boundary_0` and `upper_boundary_1`) categorize the delay as either bit "0", bit "1", or the end of the message.
- Decoded bits are collected into an 8-bit chunk to form characters, which are printed when complete. The message ends upon receiving a stop character (`.`).

### Parameters
- `log_file_name`: Logs the decoded message for validation.
- `upper_boundary_0`: Maximum delay (in milliseconds) for interpreting a "0".
- `upper_boundary_1`: Maximum delay (in milliseconds) for interpreting a "1".

---

## Covert Channel Capacity

- The capacity, in bits per second, is calculated by using a sample 128 bit message, tracking the time between the first package received and the last, and dividing the time by 128 to find the covert channel capacity.
- We found the largest possible covert channel capacity as ?? bits/sec by setting our thresholds as below:

send_0_wait: 0.1

send_1_wait: 0.4

upper_boundary_0: 0.3

upper_boundary_1: 1

Smaller threshold or wait values resulted in message corruptions.


---

## Notes

- **Docker Environment**: Ensure the code runs in the provided container environment to avoid compatibility issues.
- **Parameters in `config.json`**: All delay thresholds and log filenames must be added to the configuration file for automated testing.

This implementation utilizes inter-arrival timings, adhering to the constraints and objectives of covert channel communication. Proper parameter tuning and environment control are crucial for achieving reliable and high-capacity communication.
