from random import randint
import serial # Serial communications
import os #OS calls to control the screensaver
import pygame.midi # to generate tones
import time

class Pacman(object):
	""" The real pacman. Open serial port on initialisation. Further calls read a new line of data """
	def __init__(self):
		# Read the settings from the settings file
		settings_file = open("./config.txt")
		# Define test or live mode
		self.mode_line = settings_file.readline().rstrip('\n')
		# e.g. "/dev/ttyAMA0,9600,N,8,n"
		settings_line = settings_file.readline().rstrip('\n').split(',')
		port = settings_line[0]
		baud = eval(settings_line[1])
		par  = settings_line[2]
		byte = eval(settings_line[3])
		ceol = settings_line[4]
		if ceol == 'r':
			eol = b'\r'
		elif ceol == 'nr':
			eol = b'\n\r'
		else:
			eol = b'\n'
		# Close the settings file
		settings_file.close()
		if (self.mode_line == 'live'):
			# Open the serial port and clean the I/O buffer
			self.ser = serial.Serial()
			self.ser.port = settings_line[0]
			self.ser.baudrate = baud
			self.ser.parity = par
			self.ser.bytesize = byte
			self.ser.open()
			self.ser.flushInput()
			self.ser.flushOutput()
		else:
			file = open("pacman_sample.txt", "r")
			self.lines = file.read().split('\n')
			file.close()
		self.prevnote = 48
		# Initialize MIDI component
		instrument = 79 # Whistle
		pygame.init()
		pygame.midi.init()
		port = 0
		# global midiOutput   # It is used in other methods
		self.midiOutput = pygame.midi.Output(port, 0)
		self.midiOutput.set_instrument(instrument)
		

	def read_data(self):
		""" Reads data from pacman """
		if (self.mode_line == 'live'):
			# Get a line of data from PACMAN
			line = self.ser.readline()
		else:
			end = len(self.lines)
			start = 1
			idx = randint(start, end)
			line = self.lines[idx]
		entry = self.parse_line(line)
		return entry

	def parse_line(self, line):
		#Get the measurements
		if (line[0].isdigit()):
			p_vec = map(float,line.split())
			if (len(p_vec)>=14):
				indx = p_vec[0] #0
				dust =p_vec[10] #1
				distance = p_vec[7] #2
				t1 = p_vec[8] #3
				t2 = p_vec[9] #4
				co2 = p_vec[11] #5
				co = p_vec[12] #6
				mov = p_vec[13] #7
				co_st = p_vec[14] #8
			else:
				print("Short data line")
				print(p_vec)
				indx=-99
				dust=-99
				distance=-99
				t1=-99
				t2=-99
				co2=-99
				co=-99
				mov=-99
				co_st=-99
		else:
			print("Non numeric first character")
			print(line)
			indx=-99
			dust=-99
			distance=-99
			t1=-99
			t2=-99
			co2=-99
			co=-99
			mov=-99
			co_st=-99
		#PACMAN controlled activities
		# Deactivate screensaver with movement
		if (mov>=1):
			os.system("xscreensaver-command -deactivate") ##If there is movement ... deactivate the screensaver
		# Play a tone that changes with distance
		# http://www.derickdeleon.com/2014/07/midi-based-theremin-using-raspberry-pi.html
		""" Compute the note based on the distance measurements, get percentages of each scale and compare """
		# Config
		# you can play with these settings
		minDist = 3    # Distance Scale
		maxDist = 200
		octaves = 1
		minNote = 48   # c4 middle c
		maxNote = minNote + 12*octaves
		# Percentage formula
		fup = (distance - minDist)*(maxNote-minNote)
		fdown = (maxDist - minDist)
		note2play = int(minNote + fup/fdown)
		self.midiOutput.note_off(self.prevnote,127)
		self.midiOutput.note_on(note2play,127)
		self.prevnote = note2play
		
		return (indx, dust, distance, t1, t2, co2, co, mov, co_st)



