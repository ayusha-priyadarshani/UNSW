#!/bin/env python3

##################################################################################################################################
#
#                                         COMP3331 ASSIGNMENT
#                                      Simple Transport Protocol
#                                              sender.py
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

class STPPacket:
	def __init__(self, data, seq_num, ack_num, ack=False, syn=False, fin=False):
		self.data = data
		self.seq_num = seq_num
		self.ack_num = ack_num
		self.ack = ack
		self.syn = syn
		self.fin = fin
	
class Sender:

	# initialise sender data
	def __init__(self, sender_port, receiver_port, file, max_win, rto, flp, rlp):
		self.sender_port=int(sender_port)
		self.receiver_port = int(receiver_port)
		self.file = file      		# grab file from arg[4]
		self.max_win = int(max_win)			# max window size
		self.rto = int(rto) 		# max segment size
		self.flp = float(flp)
		#print(self.flp==1)
		self.rlp = float(rlp)

	# create UDP socket
	s = socket(AF_INET, SOCK_DGRAM)

	# Read file from input, extract data and store in class
	# NOTE: max_seg_size = max bytes carried in each STP segment

	# App-layer passing down data
	def read_file(self):
		f = open(self.file, "r")	# open file
		data = f.read()				# read file + store in data obj
		return data

	# receive packet from server, return packet
	
	def stp_rcv(self):
		data, client_add= self.s.recvfrom(self.max_win+2048)
		stp_packet=pickle.loads(data)
		#print(stp_packet)
		return stp_packet, client_add

	# create SYN
	def make_SYN(self, seq_num, ack_num):
		print("Creating SYN")
		syn = STPPacket('', seq_num, ack_num, ack=False, syn=True, fin=False)
		return syn

	# create ACK
	def make_ACK(self, seq_num, ack_num):
		print("Creating ACK")
		ack = STPPacket('', seq_num, ack_num, ack=True, syn=False, fin=False)
		return ack

	# create FIN
	def make_FIN(self, seq_num, ack_num):
		print("Creating FIN")
		fin = STPPacket('', seq_num, ack_num, ack=False, syn=False, fin=True)
		return fin

	# send segment over UDP
	def send(self, stp_packet):
		self.s.sendto(pickle.dumps(stp_packet), ('', self.receiver_port))

	# retransmit data packets
	def retransmit(self, packet):
		self.s.sendto(pickle.dumps(packet), ('', self.receiver_port))
		#sender.update_log("snd", , "", packet)
	
	# split file into partitions
	def split_data(self, data, start):
		length = len(data)
		# calculate start : end range
		end = data_progress + 1000
		#print(length, end)
		# not exceeding total size
		if end < length:
			partition = data[start:end]
		else:
			partition = data[start:length]
		
		return partition
	
	# execute forward packet loss
	def exe_forward_loss(self):
		if self.flp==1.0:
			return True
		elif self.flp==0:
			return False
		else:
			num=random.random()
			if num<self.flp:
				return True
			else:
				return False
	# execute reverse loss
	def exe_reverse_loss(self):
		if self.rlp==1.0:
			return True
		elif self.rlp==0:
			return False
		else:
			num=random.random()
			if num<self.rlp:
				return True
			else:
				return False

	# Update Sender_log.txt
	def update_log(self, action, start_time, pkt_type, packet):
		print("Updating sender log . . .")
		# grabbing header fields
		seq=packet.seq_num
		size = len(packet.data)
		
		curr_time = time.time() * 1000
		time_diff = curr_time - start_time
		seq = str(seq); size = str(size); #ack = str(ack)
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
		f = open("sender-log.txt", "a+")
		f.write(final_str)
		f.close()
	
if __name__=="__main__":
	seq_num=random.randint(0,65535)
	ack_num=0
	sendbase = 0 	# oldest un_ACK seg's first byte
	num_unacked = 0 # tracking remaining unack'd segs
	# sender states
	closed_state=True
	syn_sent_state=False
	established_state=False
	closing_state = False
	fin_wait_state=False
	
	# track states and packets
	prev_state = None
	curr_packet = None
	prev_pkt = None
	# track packet progress
	num_transmitted = 0
	num_retransmitted = 0
	num_dropped = 0
	dup_acks=0
	ack_dropped=0
	rlp_drop_count=0
	# grab args
	sender_port, receiver_port, file, max_win, rto, flp, rlp = sys.argv[1:]
	# timing vars
	curr_time = 0
	prev_time = 0
	timeout = float(rto)
	# reset sender_log.txt
	f = open("sender-log.txt","w")
	f.close()

	# App layer initiates, create socket, store app-layer file
	print("Sender initiated . . .")
	sender = Sender(sender_port, receiver_port, file, max_win, rto, flp, rlp)
	sender.s.bind(('',int(sender_port)))
	data = sender.read_file()

	buffer=[]
	ack_buffer=[]
	data_progress = 0
	data_len = len(data)
	#print(data_len)
	start_time=time.time() * 1000
	while True:
		print("start of loop")
		
		### CLOSED STATE ###
		# send SYN seg
		if closed_state == True:
			print("\n===================== STATE: CLOSED")
			
			if rlp_drop_count>0:
				seq_num-=1
			
			syn_pkt = sender.make_SYN(seq_num, ack_num)

			if sender.exe_forward_loss()==True:
				print("PACKET DROPPED")
				 
				sender.update_log("drp", start_time , "SYN", syn_pkt)
				# if flp is 1, nothing gets sent
				if sender.flp!=1:
					sender.retransmit(syn_pkt); num_unacked += 1
					#num_retransmitted+=1

					sender.update_log("snd", start_time , "SYN", syn_pkt)
					
					prev_pkt = syn_pkt
				else:
					continue
			else:
				# make and send SYN
				syn_pkt = sender.make_SYN(seq_num, ack_num)
				sender.send(syn_pkt)
				prev_pkt = syn_pkt
				
				sender.update_log("snd", start_time, "SYN",syn_pkt)
			prev_time = time.time() * 1000
			seq_num = (seq_num + 1 )% 65536
			
			closed_state = False
			syn_sent_state = True
			
		if syn_sent_state == True:
			print("\n===================== STATE: SYN SENT")
			
			if sender.exe_reverse_loss()==True:
				# reverse loss true
				print("Dropped ACK")
				drop_pkt, add=sender.stp_rcv()
				sender.update_log("drp", start_time , "ACK",drop_pkt)
				
				rlp_drop_count+=1
				closed_state=True
				syn_sent_state=False
			else:	
				#rcv ACK 
				ack_pkt, client_add = sender.stp_rcv()
				if ack_pkt.seq_num not in ack_buffer:
					ack_buffer.append(ack_pkt.seq_num)
				else:
					dup_acks+=1
				sender.update_log("rcv", start_time, "ACK", ack_pkt)
				
				# ACK received, 2-way-established
				if ack_pkt.ack == True:
					established_state = True
					syn_sent_state = False
		
		if established_state==True:
			print("CONNECTION ESTABLISHED")
			curr_time=time.time()
			time_diff= curr_time - prev_time
			
			# initialised variables
			num_unacked=0
			sliding_win_size=0
			# unacked segments present in buffer
			if len(buffer)>0:
				for i in range(0,len(buffer)-1):
					sliding_win_size+=len(buffer[i].data)
			
			while sliding_win_size<int(max_win) and data_progress < data_len:
				# prev packet exists, timeout reached -> retransmit
				if prev_pkt != None and time_diff > timeout:
					print("PACKET RETRANSMITTING")
				
					sender.retransmit(prev_pkt); num_unacked += 1
					num_retransmitted+=1
					sender.update_log("snd", start_time, "DATA",packet)
					
					prev_time = time.time() * 1000
					
					prev_pkt=None
				# make new packet and send
				else:
					partition = sender.split_data(data, data_progress)
					packet = STPPacket(partition, seq_num, ack_num, ack=False, syn=False, fin=False)

					# forward loss == False
					if sender.exe_forward_loss()!=True:
						print("PACKET SENT SUCCESSFULLY")
						# make packet
						sender.send(packet); num_unacked += 1
						prev_pkt = packet
						#increment sliding window size
						sliding_win_size+=len(packet.data)
						sender.update_log("snd", start_time, "DATA",packet)
						#add packet to unacked buffer
						buffer.append(packet)
						prev_time = time.time() * 1000
						
					# forward loss == True
					else:
						print("PACKET DROPPED")
						sender.update_log("drp", start_time , "DATA",packet)
						num_dropped += 1
						# retransmit packet
						
						sender.retransmit(packet); num_unacked += 1
						num_retransmitted+=1
						sender.update_log("snd", start_time, "DATA",packet)
						#add packet to unacked buffer
						buffer.append(packet)
						prev_time = time.time() * 1000
						sliding_win_size+=len(packet.data)
						
						prev_pkt = packet
						
					# update data progress and seq_num
					seq_num = (seq_num + len(partition))% 65536 
					data_progress += len(partition)
			
			# if whole file has been transfered, change state value
			if data_progress == data_len:
				
				closing_state = True
				established_state = False		
			
			# wait for RCV ack
			print("\n==== STATE: WAITING FOR ACK ===")
			# while all ACKs havent been received once
			while num_unacked>0:
				
				# no ACKs dropped
				if sender.exe_reverse_loss()!=True:
					ack_pkt, client_add = sender.stp_rcv()
					
					prev_pkt=None
					
					if ack_pkt.ack == True and ack_pkt.ack_num > sendbase:
						print("<<< ACK RECEIVED >>>")
						num_transmitted += 1
						sender.update_log("rcv", start_time, "ACK",ack_pkt)
						
						num_unacked-=1
						sendbase = ack_pkt.ack_num
						if num_unacked == 0:
							curr_time = time.time() * 1000
						prev_pkt=None
						buffer.pop(0)
						
				
				else:
					# drop ACK and retransmit corresponding data segment
					drop_pkt, add=sender.stp_rcv()
					sender.update_log("drp", start_time, "ACK",drop_pkt)
					ack_dropped+=1
					sender.retransmit(buffer[0])
					sender.update_log("snd", start_time, "DATA",buffer[0])
					buffer.append(buffer[0])
					buffer.pop(0)
					num_retransmitted+=1
				
				
		# entire file is sent 
		if closing_state == True:
			print("\n===================== STATE: END OF CONNECTION ")
			
			# make FIN
			# retransmit if dropped
			fin_pkt = sender.make_FIN(seq_num, ack_num)
			if sender.exe_forward_loss()!=True:
				sender.send(fin_pkt)
				prev_pkt = fin_pkt
				
			else:
				print("PACKET DROPPED!")
				
				sender.retransmit(fin_pkt)
				
				sender.update_log("drp", start_time , "FIN",packet)
				prev_pkt = fin_pkt
				
			
			sender.update_log("snd", start_time, "FIN",fin_pkt)
			
			fin_wait_state=True
			if fin_wait_state==True:
				ack_pkt, client_add = sender.stp_rcv()
				if ack_pkt.ack==True:
					sender.update_log("rcv", start_time, "ACK",ack_pkt)
					print(ack_pkt.seq_num)
					sender.s.close()
					print("CLOSED")
					break
		
	# add statistics to log file
	
	
	data = "Original data sent:  		 {} bytes\n".format(data_len)
	ack = "Original data acked:  		 {} bytes\n".format(data_progress)
	seg_sent = "Original segments sent:  		 {}\n".format(num_transmitted)
	seg_retrans = "Retransmitted segments sent:     {}\n".format(num_retransmitted)
	dup_acks= "Duplicate ACKS received: 	  	 {}\n".format(dup_acks)
	pkt_dropped = "Data segments Dropped: 	 	     {}\n".format(num_dropped)
	ack_dropped = "Ack segments Dropped:  	         {}\n". format(ack_dropped)
	
	final_str = "\n" + data + ack + seg_sent + seg_retrans + dup_acks + pkt_dropped + ack_dropped
	
	f=open("sender-log.txt","a+")
	f.write(final_str)
	f.close()
		