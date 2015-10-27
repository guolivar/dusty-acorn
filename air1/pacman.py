from random import randint
import serial # Serial communications

class Pacman(object):
	""" The real pacman. Open serial port on initialisation. Further calls read a new line of data """
	def __init__(self):
		# Read the settings from the settings file
		settings_file = open("./config.txt")
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
		# Open the serial port and clean the I/O buffer
		ser = serial.Serial()
		ser.port = settings_line[0]
		ser.baudrate = baud
		ser.parity = par
		ser.bytesize = byte
		ser.open()
		ser.flushInput()
		ser.flushOutput()

	def read_data(self):
		""" Reads data from pacman """
		# Get a line of data from PACMAN
		line = ser.readline()
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
