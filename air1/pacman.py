from random import randint

class Pacman(object):
	""" The real pacman """
	pass

	def read_data(self):
		""" Reads data from pacman """
		return "TODO"

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
