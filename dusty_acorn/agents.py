# -*- coding: utf-8 -*-
"""Application agents."""

import json
import time
from datetime import datetime
from multiprocessing import Queue
from threading import Thread

from dusty_acorn.pacman import Pacman


class Agent(Thread):
    """An agent.

    This is a thread, used as the agent, responsible for listen to events to/from the UI, and interact with message
    queues."""

    def __init__(self, tasks_queue, results_queue):
        """Constructor.

        :param tasks_queue: task queue
        :type tasks_queue: Queue
        :param results_queue: result queue
        :type results_queue: Queue
        """
        Thread.__init__(self)
        self.tasks_queue = tasks_queue
        self.results_queue = results_queue

        self.pacman = None

        # init agent settings, flags, etc
        self.pc_time = datetime.now()
        self.has_been_initialized = False
        self.running = True
        print('Agent initialised')
        print(self.pc_time)

    def close(self):
        """ Deletes any object no needed any more, close connections, etc """
        self.running = False
        print('agent exited')

    def init(self):
        """Called once, in the first run of the agent."""

        print('Program started.')
        self.send_message_to_ui('Program started.')

        self.send_message_to_ui('Creating pacman device...')
        self.pacman = Pacman()

    def send_message_to_ui(self, message):
        """Sends messages to the UI, via the result queue."""

        data = dict()
        data['message'] = message
        data['type'] = 'message'
        self.results_queue.put(data)

    def run(self):
        """Contains the main logic of the agent.

        Handles messages received from the UI (task_queue), and sends data back to the UI (result_queue)."""

        while self.running:
            if not self.has_been_initialized:
                self.init()
                self.has_been_initialized = True
            # look for incoming tornado request
            if not self.tasks_queue.empty():
                task = self.tasks_queue.get()

                # You can view the content of this message in the console where you started the program
                print("Agent received from web: " + task)

                data = json.loads(task)

                # this information comes from the HTML page. You could submit different
                # if data['type'] == 'action_xyz':
                #     print "TOGGLED!"
                #     if self.__file__ == 'abc':
                #         pass

            # read the serial data
            metrics = self.get_metrics()
            self.results_queue.put(metrics)
            time.sleep(1)

    def get_metrics(self):
        """This method must return a dict, that represents the metrics collected by the agent."""
        return {
            'type': 'heartbeat',
            'time': datetime.now().strftime('%H:%M:%S'),
            'pacman_data': self.pacman.read_data()
        }
