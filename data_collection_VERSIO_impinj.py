#!/usr/bin/env python

import signal
import argparse
import sys
import json
import sqlite3
import time
import os
import platform

import requests
try:
	from urlparse import urljoin
except ImportError:
	from urllib.parse import urljoin

import pygame
from threading import Thread

DB_FILENAME = 'dataset.db'
READER_PARAMS_QUERY = "CREATE TABLE IF NOT EXISTS DATAPOINTS (TIMESTAMP varchar(255), READER_HOSTNAME varchar(255), TAGID varchar(255), ANTENNA_NAME varchar(255), PEAK_RSSI FLOAT, FREQUENCY varchar(255), PHASE FLOAT)"




# Set up the drawing window
mult=10

X=0
Y=0

def map_range(x,a,b,c,d):
   y=(x-a)/(b-a)*(d-c)+c
   return y


def clear_screen():
	"""Clears the console screen."""
	if platform.system() == "Windows":
		os.system('cls')
	else:
		os.system('clear')

def update_circle_position(width, height, start_x, start_y, end_x, end_y, steps=10):
	"""
	Updates the circle's position from a starting point to an ending point.
	
	Args:
	width (int): The width of the box.
	height (int): The height of the box.
	start_x (int): The starting x-coordinate of the circle.
	start_y (int): The starting y-coordinate of the circle.
	end_x (int): The ending x-coordinate of the circle.
	end_y (int): The ending y-coordinate of the circle.
	steps (int): Number of steps to move from start to end.
	"""
	dx = (end_x - start_x) / steps
	dy = (end_y - start_y) / steps
	for step in range(steps + 1):
		clear_screen()
		current_x = int(start_x + dx * step)
		current_y = int(start_y + dy * step)
		draw_box_and_circle(width, height, current_x, current_y)
		time.sleep(0.5)

def signal_handler(signal, frame):
	print('Stopped execution')
	sys.exit(0)

def drawpygame():
	global X,Y,mult
	pygame.init()
	screen = pygame.display.set_mode([100*mult, 100*mult])
	run=True
	while run:
		for event in pygame.event.get():
			screen.fill((0, 255, 0))
			print("X",X,"Y",Y)
			pygame.draw.circle(screen, (0, 0, 255), (int(X*mult),int(Y*mult) ), 50)
			pygame.display.update()
			#time.sleep(0.01)
			if event.type == pygame.QUIT:
				run=False
				
	pygame.quit()



def main():

	parser = argparse.ArgumentParser(description='A script that requires an IP address as an argument.')
	parser.add_argument('--IP', type=str, required=True, help='The IP address to be processed')
	
	args = parser.parse_args()
	
	if not args.IP:
		print("Error: IP address not specified.")
		sys.exit(1)
	
	# If IP is specified, continue with the rest of the script
	ip_address = args.IP

	global X,Y,mult

	#thread = Thread(target = drawpygame)
	#thread.start()
	
	# Handle Ctrl+C interrupt
	signal.signal(signal.SIGINT, signal_handler)


	# hostname = 'http://impinj-14-02-9f/'
	hostname = 'http://'+ip_address+'/'

	session = requests.Session()
	session.auth = ("root", "impinj")

	conn = sqlite3.connect(DB_FILENAME)
	c = conn.cursor()
	# Create DB table
	c.execute(READER_PARAMS_QUERY)

	session.post(urljoin(hostname, 'api/v1/profiles/stop')) # Stop the active preset
	#session.post(urljoin(hostname, 'api/v1/profiles/inventory/presets/default/start')) # Start the default preset
	session.post(urljoin(hostname, 'api/v1/profiles/inventory/presets/TestQuelic/start')) # Start the default preset
	i = 1
	for event in session.get(urljoin(hostname, 'api/v1/data/stream'), stream=True).iter_lines(): # Connect to the event stream

		
		# If information is empty, skip iteration
		if event == b'':
			continue
		# Insert values
		message=event.decode()

		#print(message)
		try:
			timestamp = json.loads(event)["timestamp"]
			readerHostname = json.loads(event)["hostname"]
			if b'tagInventoryEvent' in event:

				tagInventoryEvents = json.loads(event)["tagInventoryEvent"]
				if tagInventoryEvents["antennaName"]=='Laird_8dBci':
					#print(tagInventoryEvents["epcHex"])
					if tagInventoryEvents["epcHex"]=='E280689400004001F59314C9':
						#c.execute("insert into datapoints values (?, ?, ?, ?, ?, ?, ?)", [timestamp, readerHostname, tagInventoryEvents["epcHex"], tagInventoryEvents["antennaName"], tagInventoryEvents["peakRssiCdbm"]/100, tagInventoryEvents["frequency"], tagInventoryEvents["phaseAngle"]])
						
						#print(tagInventoryEvents)
						#print(tagInventoryEvents["peakRssiCdbm"])
						Y=tagInventoryEvents["peakRssiCdbm"]
						Y=map_range(Y,-2100,-7000,0,100)
				if tagInventoryEvents["antennaName"]=='SP11':
					#print(tagInventoryEvents["epcHex"])
					if tagInventoryEvents["epcHex"]=='E280689400004001F59314C9':
						X=tagInventoryEvents["peakRssiCdbm"]
						X=map_range(X,-3400,-7000,0,100)
			
			#if i == 4000:
			#	break
			#i = i + 1
		except Exception as e:
			pass
		
		#loop_update_circle_position(X, Y)
		#update_circle_position(100, 100, 1, 1, 18, 8, 20)
		#pygame
		#screen.fill((255, 255, 255))

		# Draw a solid blue circle in the center
		
		#time.sleep(0.01)

	conn.commit()
	conn.close()
	session.post(urljoin(hostname, 'api/v1/profiles/stop')) # Stop the active preset
	# Done! Time to quit.
	

if __name__ == "__main__":
	main()