# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 12:35:01 2015

@author: gustavo
"""

from pygame import ini
import pygame.midi
from time import sleep

# Parameters that you can change
instrument = 0
velocity = 127

# Initialize the Pygame and pygame.midi modules
pygame.init()
pygame.midi.init()

# This port number seems the only one to work
port = 0
latency = 1

# Set parameters
midiOutput = pygame.midi.Output(port, latency)
midiOutput.set_instrument(instrument)

# Play all 128 notes
for note in range(0, 127):
  midiOutput.note_on(note, velocity)
  sleep(.25)
  midiOutput.note_off(note, velocity)

# close the handler and quit midi
del midiOutput
pygame.midi.quit()