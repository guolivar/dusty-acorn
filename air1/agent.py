# -*- coding: utf8 -*-

# base imports
import time
import datetime
import json

# the agent is a thread
from threading import Thread

# choose which pacman to use dynamically
import importlib
serial_device_class = "air1.pacman.Pacman"
module_name, class_name = serial_device_class.rsplit('.', 1)
SerialDeviceClass = getattr(importlib.import_module(module_name), class_name)

class Agent(Thread):
    """ An agent. Tis a thread, used as the agent, responsible for listen to events to/from the UI, and interact with message queues appropriately """

    def __init__(self, taskQ, resultQ):
        """ Constructor """

        Thread.__init__(self)
        self.taskQ = taskQ
        self.resultQ = resultQ

        self.pacman = False
        
        # init agent settings, flags, etc
        self.pc_time = datetime.datetime.now()
        self.has_been_initialized = False
        self.running = True
        print('Agent initialised')
        print(self.pc_time)

    def close(self):
        """ Deletes any object no needed any more, close connections, etc """

        # self.e.__del__
        self.running = False
        print('agent exited')

    def init(self):
        """ Called only once, in the first run of the agent """

        print('Program started.')
        self.send_message_to_ui('Program started.')
        
        self.send_message_to_ui('Creating pacman device...')
        self.pacman = SerialDeviceClass ()

    def send_message_to_ui(self, message):
        """ Sends messages to the UI, via the result queue """

        data = dict()
        data['message'] = message
        data['type'] = 'message'
        self.resultQ.put(data)

    def run(self):
        """ Contains the main logic of the agent, handling messages received from the UI (taskQ), and sending data back to the UI (resultQ) """
 
        while self.running:
            if not self.has_been_initialized:
                self.init()
                self.has_been_initialized = True
            # look for incoming tornado request
            if not self.taskQ.empty():
                task = self.taskQ.get()

                # You can view the content of this message in the console where you started the program
                print "Agent received from web: " + task

                data = json.loads(task)

                # this information comes from the HTML page. You could submit different
                # if data['type'] == 'action_xyz':
                #     print "TOGGLED!"
                #     if self.__file__ == 'abc':
                #         pass

            # read the serial data
            metrics = self.get_metrics()
            self.resultQ.put(metrics)
            time.sleep(1)

    def get_metrics(self):
        """ This method must return a dict, that represents the metrics collected by the agent """

        metrics = dict()

        metrics['type'] = 'heartbeat' # message type
        metrics['time'] = datetime.datetime.now().strftime('%H:%M:%S')
        pacman_data = self.pacman.read_data()
        metrics['pacman_data'] = pacman_data
 
        return metrics

    
