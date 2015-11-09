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
		# Play a sound file that changes with distance
		print(distance)
		if distance < 380:
			os.system('mpg123 -q 442.mp3 &')
		elif distance < 650:
			os.system('mpg123 -q 454.mp3 &')
		else:
			os.system('mpg123 -q 466.mp3 &')
		return (indx, dust, distance, t1, t2, co2, co, mov, co_st)

class FakePacman(Pacman):
	""" A fake Pacman. Reads pacman_sample.txt on initialisation. Further calls will return any random entry. """

	def __init__(self):
		file = open("pacman_sample.txt", "r")
		self.lines = file.read().split('\n')
		file.close()

	def read_data(self):
		end = len(self.lines)
		start = 1
		idx = randint(start, end)
		line = self.lines[idx]

		entry = self.parse_line(line)
		return entry

	def parse_line(self, line):
		#Get the measurements
		p_vec = map(float,line.split())
		indx = p_vec[0] #0
		dust = p_vec[10] #1
		distance = p_vec[7] #2
		t1 = p_vec[8] #3
		t2 = p_vec[9] #4
		co2 = p_vec[11] #5
		co = p_vec[12] #6
		mov = p_vec[13] #7
		co_st = p_vec[14] #8

		return (indx, dust, distance, t1, t2, dust, co2, co, mov, co_st)

