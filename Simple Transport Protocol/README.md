## Overview
For this assignment, we were required to implement a Simple Transport Protocol (STP) – a reliable transport protocol over the UDP protocol. Features like two-way handshake, timeout, sliding window protocol, forward packet loss, backward packet loss had to be executed by our program. 

## Construction and Program Design
Language: Python
I started off by building STP Packet, sender and receiver classes. I built a main function, stored command-line arguments in variables, initialised other variables, and passed them to their respective classes (if any) to confirm proper functioning. 

After the classes were established, I added basic features required for STP transfer of a small file, such as state variables and functions like stp_rcv, make_SYN, make_ACK, send, add_data, update_log. To test whether the functions written were performing according to the guideline, I built a basic Two-Way handshake code along with a basic file transfer snippet. 

Once the foundation of the program was concrete, I added functions like retransmit, make_FIN, split_data, exe_forward_loss, exe_reverse_loss. 
Addition of more features lead to an increase in the complexity of the overall program, but after meticulous debugging and adjustments a successful Stop-and-Wait protocol was built over both reliable and unreliable channels.

To conquer the last milestone, I implemented Sliding-Window protocol over a reliable and unreliable channel. Buffers  were added for comfortable data transfer while simulating forward and reverse packet loss.

