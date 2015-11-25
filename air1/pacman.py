from random import randint
import serial # Serial communications
import os #OS calls to control the screensaver and play sounds
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
		# Close the settings file
		settings_file.close()
		if (self.mode_line == 'live'):
			# If live ... open the serial port
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
			# If test ... open and read sample file
			file = open("pacman_sample.txt", "r")
			self.lines = file.read().split('\n')
			file.close()
		# Initialise the activity counter
		self.movlist = [0] * 60
		# Initialise the frames for scaling Output
		self.frameCO2 = [0] * 60
		self.frameDUST = [0] * 60
		self.frameTEMP = [10] * 60
		# Initialise max/min for scaling Output
		self.frameCO2 = [-2500] + self.frameCO2[:-1]
		self.frameDUST = [3000] + self.frameDUST[:-1]
		self.frameTEMP = [30] + self.frameTEMP[:-1]
		# Initialise the max/min for scales
		self.maxCO2 = max(self.frameCO2)
		self.minCO2 = min(self.frameCO2)
		self.maxDUST = max(self.frameDUST)
		self.minDUST = min(self.frameDUST)
		self.maxTEMP = max(self.frameTEMP)
		self.minTEMP = min(self.frameTEMP)

		# Initialise the CO handling containers
		self.entry = self.parse_line("a")
		self.rawentry = self.entry
		self.prev_entry = self.entry
		self.prev_rawentry = self.entry

	def read_data(self):
		""" Reads data from pacman """
		if (self.mode_line == 'live'):
			# Get a line of data from PACMAN
			line = self.ser.readline()
		else:
			end = len(self.lines) - 1
			start = 0
			idx = randint(start, end)
			line = self.lines[idx]
		self.entry = self.parse_line(line)
		# TODO deal with CO data ... the code below throws errors
		#print(self.entry)
		#self.entry = self.rawentry
		#print(self.entry)
		#print(self.prev_entry)
		#if (self.entry[8]==1) & (self.prev_entry[8]==2):
			#self.entry = self.entry[0:5] + (self.prev_rawentry[6],) + self.entry[7:8]
		#else:
			#self.entry = self.entry[0:5] + (self.prev_entry[6],) + self.entry[7:8]
		#self.prev_rawentry = self.rawentry
		#self.prev_entry = self.entry
		print(self.entry)
		return self.entry

	def parse_line(self, line):
		#Get the measurements
		if len(line) >0:
			if (line[0].isdigit()):
				p_vec = map(float,line.split())
				if (len(p_vec)>=14):
					indx = p_vec[0] #0
					dust =p_vec[10] #1
					distance = p_vec[7] #2
					t1 = p_vec[8] #3
					t2 = p_vec[9] #4
					co2 = -1*p_vec[11] #5
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
		else:
			print("Line too short")
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
		if (1>=1):
			os.system("xscreensaver-command -deactivate &") ##If there is movement ... deactivate the screensaver
		# Activate screensaver when there is little movement (50% or less in the last minute)
		self.movlist = [mov] + self.movlist[:-1]
		activity = sum(self.movlist)/len(self.movlist)
		if (1 < 0.5):
			os.system("xscreensaver-command -activate &") ##If there is little movement ... activate the screensaver
		# Update the frame of data for scale
		self.frameCO2 = [co2] + self.frameCO2[:-1]
		self.frameDUST = [dust] + self.frameDUST[:-1]
		self.frameTEMP = [t1] + self.frameTEMP[:-1]
		# Calculate the max/min for each stream only for valid data lines
		if (indx>0):
			self.maxCO2 = max(self.frameCO2)
			self.minCO2 = min(self.frameCO2)
			self.maxDUST = max(self.frameDUST)
			self.minDUST = min(self.frameDUST)
			self.maxTEMP = max(self.frameTEMP)
			self.minTEMP = min(self.frameTEMP)
		# C D E F G A B
		print(distance)
		#         0    1       2       3   4   5    6   7         8       9      10       11       12      13       14
		return (indx, dust, distance, t1, t1, co2, co, activity, co_st, self.minCO2, self.maxCO2, self.minDUST, self.maxDUST, self.minTEMP, self.maxTEMP)