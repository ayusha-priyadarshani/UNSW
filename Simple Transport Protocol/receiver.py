#!/bin/env python3

##################################################################################################################################
#
#                                         COMP3331 ASSIGNMENT 
#                                      Simple Transport Protocol
#                                             receiver.py
#
#                                       by  Ayusha Priyadarshani
#                                               z5452643
#
#                                              11-04-2024
#                    
##################################################################################################################################

import sys
import time
from socket import *
import pickle
import random
import threading


class STPPacket:
    def __init__(self, data, seq_no, ack_no, ack=False, syn=False, fin=False):
        self.data=data
        self.seq_num=seq_no
        self.ack_num=ack_no
        self.ack=ack
        self.syn=syn
        self.fin=fin

class receiver_obj:
    def __init__(self, sender_port, receiver_port, file, max_win):
        self.sender_port=int(sender_port)
        self.receiver_port=int(receiver_port)
        file=file+".txt"
        self.file=file
        self.max_win=int(max_win)
    
    s = socket(family=AF_INET, type=SOCK_DGRAM)

    # receives data from port
    def stp_rcv(self):
        data, client_add= self.s.recvfrom(self.max_win+2048)
        stp_packet=pickle.loads(data)
        
        return stp_packet, client_add
    
    # opens file and adds split data received
    def add_data(self,data):
        
        f = open(file,"a+")
        f.write(data)
        f.close()

    # make ACK segments
    def make_ACK(self,seq_no,ack_no):
        ack=STPPacket('',seq_no,ack_no,ack=True, syn=False, fin=False)
        return ack

    # send ACK segments
    def send(self, stp_packet):
        self.s.sendto(pickle.dumps(stp_packet), ('', self.sender_port))
    
    # close socket
    def close(self):
        print("Closed!")
        self.s.close()
    
    # Update receiver-log.txt
    def update_log(self, action, start_time, pkt_type, packet):
		# grabbing header fields
        seq=packet.seq_num
        size = len(packet.data)
        
        seq = str(seq); size = str(size); 

        curr_time = time.time() * 1000
        time_diff = curr_time - start_time

        # init arrays of args and col lens
        col_lens = [5, 5, 8, 10, 5]
        args = [action, str(round(time_diff,1)), pkt_type, seq, size]
        # build string
        final_str = ""
        counter = 0
        # loop through columns
        for c in col_lens:
            arg_len = len(args[counter])
            space_len = c - arg_len
            space_str = ""
            # add whitespace for each column
            while arg_len < c:
                space_str += " "
                arg_len += 1
            # append each col to line
            final_str += str(args[counter]) + space_str
            counter += 1
        # add newline to final str
        final_str += "\n"
        #print(final_str)
        # append complete line to log
        f = open("receiver-log.txt", "a+")
        f.write(final_str)
        f.close()

# receiver thread
def recv_thread(control):
    while control.is_alive:
        try:
            nread = receiver.s.recv(2048)
            #ok=1
        except TypeError:
            control.is_alive = False
            break
        except ConnectionRefusedError:
            print(f"recv: connection refused by {control.host}:{control.port}, shutting down...", file=sys.stderr)
            control.is_alive = False
            break

# timer thread
def timer_thread():
    nread = receiver.s.recv(2048)
    #print(f"{control.run_time} timer expired")
    #control.is_alive=False
    return

if __name__=="__main__":
    # fetch arguments
    receiver_port=sys.argv[1]
    sender_port=sys.argv[2]
    store_in_file=sys.argv[3]
    max_win=sys.argv[4]

    seq_num=random.randint(0,65536)
    ack_num=0
    dup_data=0
    num_rec=0
    dup_acks=0

    # initiliased states
    closed_state=True
    listen_state=False
    established_state=False
    time_wait_state=False
    
    # initiliased socket
    print("<<<<<<<<<<<<<< STATE = CLOSED      >>>>>>>>>>>>>>>\n")
    receiver=receiver_obj(sender_port,receiver_port,store_in_file,max_win)
    receiver.s.bind(('',int(receiver_port)))
    print("Initialised connection...\n")

    # set state values 
    closed_state=False
    listen_state=True
    established_state=False
    time_wait_state=False
    

    data_progress=0
    seq_list=[]

    # reset file and log
    file=store_in_file+".txt"
    f = open("receiver-log.txt","w")
    g = open(file,"w")
    f.close()
    g.close()
    
    while True:
        if listen_state==True:
            print("<<<<<<<<<<<<<< STATE = LISTEN      >>>>>>>>>>>>>>>\n")
            syn_pkt, client_add = receiver.stp_rcv()
            start_time= time.time() * 1000
            print("Connection established!\n")
            # wait for SYN
            receiver.update_log("rcv", start_time, "SYN",syn_pkt)
            if syn_pkt.syn == True:
                seq_num = (syn_pkt.seq_num + 1) % 65536
                ack_num+=1
                # make and send ACK
                ack_pkt = receiver.make_ACK(seq_num, ack_num)
                receiver.send(ack_pkt)
                
                receiver.update_log("snd", start_time, "ACK",ack_pkt)
                listen_state=False
                established_state=True
        # start clock
        start_time= time.time() * 1000
        if established_state==True:
            print("<<<<<<<<<<<<<< STATE = ESTABLISHED >>>>>>>>>>>>>>>\n")
            while True:
                packet, client_addr = receiver.stp_rcv()
                curr_time = time.time() * 1000
                time_diff = curr_time - start_time
                
                ack_num+=1
                data = packet.data
                
                # if FIN received
                if packet.fin == True:
                    print("FIN initiated by sender . . .")
                    receiver.update_log("rcv", start_time, "FIN",packet)
                    time_wait_state=True
                    established_state= False
                    break
                
                #if another SYN received
                elif packet.syn==True:
                    print("Duplicate SYN received . . .")
                    seq_num = ( syn_pkt.seq_num + 1 ) % 65536
                    ack_num+=1
                    ack_pkt = receiver.make_ACK(seq_num, ack_num)
                    #dup_acks+=1
                    receiver.update_log("rcv", start_time, "SYN",syn_pkt)
                    receiver.send(ack_pkt)
                     
                    receiver.update_log("snd", start_time, "ACK",ack_pkt)
                    listen_state=False
                    established_state=True

                # Receive normal seg, check pkt_sn = rcv_sn
                # Send ACK for packet, increment seq_num by sizeof payload
                elif packet.seq_num not in seq_list:
                    receiver.update_log("rcv", start_time, "DATA",packet)
                    print("PACKET OKAY, SEND ACK")
                    # acknowledge seg, increment seq_num (indicate sizeof payload ack-ing)
                    print(seq_num)
                    print(packet.seq_num)
                    
                    seq_num+=len(packet.data) % 65536

                    ack_pkt = receiver.make_ACK(seq_num, ack_num)
                    receiver.send(ack_pkt)
                    
                    receiver.update_log("snd", start_time, "ACK",ack_pkt)
                    # add payload to final file
                    data_progress += len(data)
                    print(data_progress)
                    receiver.add_data(data)
                    num_rec+=1
                    seq_list.append(packet.seq_num)
                else:
                    print("DUPLICATE SEGMENT RECEIVED")
                    dup_acks+=1
                    print(packet.seq_num)
                    seq_num=(packet.seq_num + len(packet.data)) % 65536
                    
                    receiver.update_log("rcv", start_time, "DATA",packet)
                    ack_pkt = receiver.make_ACK(seq_num, ack_num)
                    receiver.send(ack_pkt)
                    dup_data+=1
                    receiver.update_log("snd", start_time, "ACK",ack_pkt)
                    
                    # add payload to final file

        # initialised connection end
        if time_wait_state == True:
            print("\n<<<<<<<<<<<<<< STATE = TIME WAIT   >>>>>>>>>>>>>>>\n")
            seq_num = (packet.seq_num +1) % 65536
            ack_num+=1
            ack_pkt = receiver.make_ACK(seq_num, ack_num)
            
            receiver.send(ack_pkt)
            receiver.update_log("snd", start_time, "ACK",ack_pkt)
            
            # start timer 
            receiver.s.settimeout(2)
            try:
                new, add = receiver.s.recv(2048)
                # if another FIN received, send ACK and close connection
                if new.fin==True:
                    print("Duplicate FIN received . . .")
                    receiver.update_log("rcv", start_time, "FIN",packet)
                    seq_num = (new.seq_num + 1) % 65536
                    ack_num+=1
                    ack_pkt = receiver.make_ACK(seq_num, ack_num)
                    
                    receiver.send(ack_pkt)
                     
                    receiver.update_log("snd", start_time, "ACK",ack_pkt)
                    closed_state=True
                    time_wait_state=False
            # no duplicate FIN received
            except TimeoutError:
                closed_state=True
                time_wait_state=False
            
        # close connection
        if closed_state==True:
            print("Connection closed")
            print("\n<<<<<<<<<<<<<< STATE = CLOSED   >>>>>>>>>>>>>>>\n")
            break

    
    # add statistics to log file
    data = "Original data received:  		     {} bytes\n".format(data_progress)
    seg_rec = "Original segments received:  	    	 {}\n".format(num_rec)
    dup_data= "Duplicate data segments received: 	  	 {}\n".format(dup_data)
    dup_acks= "Duplicate ack segments sent:  	         {}\n". format(dup_acks)

    final_str = "\n" + data + seg_rec + dup_data + dup_acks 
	
    f=open("receiver-log.txt","a+")
    f.write(final_str)
    f.close()