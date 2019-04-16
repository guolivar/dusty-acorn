# -*- coding: utf-8 -*-
# Routine to parse the data line received from the sensors
# 20160705
#	Changed the format of the data from the sensor.
#	New dust sensor with more data and re-ordered the data channels

import time
from random import randint

import serial  # Serial communications


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
        par = settings_line[2]
        byte = eval(settings_line[3])
        ceol = settings_line[4]
        # Close the settings file
        settings_file.close()
        # Set the initial time for data storage
        self.datapath = "../data/"
        self.timestamp = None
        self.entry = None
        self.rec_time = time.gmtime()
        if self.mode_line == 'live':
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
            with open("pacman_sample.txt", "r") as file:
                self.lines = file.read().split('\n')
        # Initialise the activity counter
        self.movlist = [0] * 60
        # Initialise the frames for scaling Output
        self.framePM1 = [0] * 60
        self.framePM10 = [0] * 60
        self.frameCO2 = [0] * 60
        self.frameDUST = [0] * 60
        self.frameTEMP = [10] * 60
        # Initialise max/min for scaling Output
        self.frameCO2 = [-2500] + self.frameCO2[:-1]
        self.frameDUST = [300] + self.frameDUST[:-1]
        self.frameTEMP = [30] + self.frameTEMP[:-1]
        # Initialise the max/min for scales
        self.maxCO2 = max(self.frameCO2)
        self.minCO2 = min(self.frameCO2)
        self.maxDUST = max(self.frameDUST)
        self.minDUST = min(self.frameDUST)
        self.maxTEMP = max(self.frameTEMP)
        self.minTEMP = min(self.frameTEMP)

    def read_data(self):
        """ Reads data from pacman """
        if self.mode_line == 'live':
            # Get a line of data from PACMAN
            line = self.ser.readline()
        else:
            end = len(self.lines) - 1
            start = 0
            idx = randint(start, end)
            line = self.lines[idx]
        self.entry = self.parse_line(line)
        # print(self.entry)
        return self.entry

    def parse_line(self, line):
        # Get the measurements
        # Data line is:
        # PM1
        # PM2.5
        # PM10
        # TSIPM1
        # TSIPM2.5
        # TSIPM10
        # Data7
        # Data8
        # Data9
        # Distance
        # Temperature
        # RH
        # CO2
        err_value = -99
        if len(line) > 0:
            if line[0].isdigit():
                p_vec = list(map(float, line.split()))
                if len(p_vec) >= 13:
                    pm1 = p_vec[0]  # 0
                    dust = p_vec[1]  # 1
                    pm10 = p_vec[2]  # 2
                    distance = p_vec[9]  # 3
                    t1 = p_vec[10]  # 4
                    rh = p_vec[11]  # 5
                    co2 = -1 * p_vec[12]  # 6
                else:
                    print("Short data line")
                    print(p_vec)
                    pm1 = err_value  # 0
                    dust = err_value  # 1
                    pm10 = err_value  # 2
                    distance = err_value  # 3
                    t1 = err_value  # 4
                    rh = err_value  # 5
                    co2 = err_value  # 6
            else:
                print("Non numeric first character")
                print(line)
                pm1 = err_value  # 0
                dust = err_value  # 1
                pm10 = err_value  # 2
                distance = err_value  # 3
                t1 = err_value  # 4
                rh = err_value  # 5
                co2 = err_value  # 6
        else:
            print("Line too short")
            print(line)
            pm1 = err_value  # 0
            dust = err_value  # 1
            pm10 = err_value  # 2
            distance = err_value  # 3
            t1 = err_value  # 4
            rh = err_value  # 5
            co2 = err_value  # 6
        # PACMAN controlled activities
        # Deactivate screensaver when something is close by (1.5m)
        # if (distance<150):
        # os.system("xscreensaver-command -deactivate &") #If something is close by... deactivate the screensaver
        # Update the frame of data for scale
        self.frameCO2 = [co2] + self.frameCO2[:-1]
        self.frameDUST = [pm10] + self.frameDUST[:-1]
        self.frameTEMP = [t1] + self.frameTEMP[:-1]
        # Calculate the max/min for each stream only for valid data lines
        if pm10 > 0:
            self.rec_time = time.gmtime()
            self.timestamp = time.strftime("%Y/%m/%d %H:%M:%S GMT", self.rec_time)
            self.maxCO2 = max(self.frameCO2)
            self.minCO2 = min(self.frameCO2)
            self.maxDUST = max(self.frameDUST)
            self.minDUST = min(self.frameDUST)
            self.maxTEMP = max(self.frameTEMP)
            self.minTEMP = min(self.frameTEMP)
            file_line = self.timestamp + ',' + str(pm1) + ',' + str(dust) + ',' + str(pm10) + ',' + str(
                distance) + ',' + str(t1) + ',' + str(rh) + ',' + str(co2)
            # We have data so we save it
            current_file_name = self.datapath + time.strftime("%Y%m%d.txt", self.rec_time)
            current_file = open(current_file_name, "a")
            current_file.write(file_line + "\n")
            current_file.flush()
            current_file.close()
        # C D E F G A B
        # print(co2)
        #         0    1    2       3      4   5    6        7            8            9           10            11            12
        print(pm1, dust, pm10, distance, t1, rh, co2, self.minCO2, self.maxCO2, self.minDUST, self.maxDUST,
              self.minTEMP, self.maxTEMP)
        return (
            pm1, dust, pm10, distance, t1, rh, co2, self.minCO2, self.maxCO2, self.minDUST, self.maxDUST, self.minTEMP,
            self.maxTEMP)
