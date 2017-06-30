'''
Simple simultaneous network control of Bonsai and OpenEphys.
Dependencies:
1. pyOSC
2. SimpleOSC
'''

import argparse
from simpleOSC import initOSCClient, sendOSCMsg
import zmq
import random
import sys
import time

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--bonsaiIP", default="127.0.0.1", help="The IP of Bonsai machine")
	parser.add_argument("--bonsaiPort", type=int, default=2323, help="The port Bonsai is listening on")
	parser.add_argument("--oeIP", default="10.153.170.52", help="The IP of OpenEphys machine")
	parser.add_argument("--oePort", default='5556', help="The port OpenEphys is listening on")
	parser.add_argument("--mode", default='start', help="start or stop")
	
	args = parser.parse_args()
	
	context = zmq.Context()
	socket = context.socket(zmq.REQ)
	socket.connect("tcp://%s:%s" % (args.oeIP, args.oePort))
	
	if args.mode == 'start':
		initOSCClient(args.bonsaiIP,args.bonsaiPort)
		sendOSCMsg("/number", [1])
		socket.send("StartRecord CreateNewDir=1")
		socket.recv_string()
	elif args.mode == 'stop':
		initOSCClient(args.bonsaiIP,args.bonsaiPort)
		sendOSCMsg("/number", [2])
		socket.send("StopRecord")
		socket.recv_string()
	elif args.mode == 'event':
		initOSCClient(args.bonsaiIP,args.bonsaiPort)
		sendOSCMsg("/number", [3])
		socket.send("Event")
		socket.recv_string()		