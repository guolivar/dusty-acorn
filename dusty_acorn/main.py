#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing
import os
import sys

import tornado.ioloop
from tornado.httpserver import HTTPServer
from tornado.options import define, options, parse_command_line
from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler

from dusty_acorn.agents import Agent

define("port", default=8080, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")


class IndexHandler(RequestHandler):

    def get(self):
        self.render("index.html", app_name='Air 1')


class IndexHandler2(RequestHandler):

    def get(self):
        self.render("index2.html", app_name='Air 1')


class GridHandler(RequestHandler):

    def get(self):
        self.render("grid.html", app_name='Air 1')


# /bars.html
class BarsHandler(RequestHandler):

    def get(self):
        self.render("bars.html", app_name='Air 1')


# /distance.html
class DistanceHandler(RequestHandler):

    def get(self):
        self.render("distance.html", app_name='Air 1')


# /dust.html
class DustHandler(RequestHandler):

    def get(self):
        self.render("dust.html", app_name='Air 1')


# /temperature.html
class TempHandler(RequestHandler):

    def get(self):
        self.render("temperature.html", app_name='Air 1')


class TempQHandler(RequestHandler):

    def get(self):
        self.render("temperature_qual.html", app_name='Air 1')


# /RH.html
class RhHandler(RequestHandler):

    def get(self):
        self.render("rh.html", app_name='Air 1')


# /co2.html
class CO2Handler(RequestHandler):

    def get(self):
        self.render("co2.html", app_name='Air 1')


# /co2_rel.html
class CO2qualHandler(RequestHandler):

    def get(self):
        self.render("co2_qual.html", app_name='Air 1')


# websockets
clients = []


class MetricsHandler(WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self, *args):
        print('New connection!')
        clients.append(self)
        data = dict()
        data['message'] = 'WebSocket connected!'
        data['type'] = 'message'
        self.write_message(data)

    def on_close(self):
        print("WebSocket closed!")
        if self in clients:
            clients.remove(self)

    def on_message(self, message):
        data = dict()
        data['message'] = 'Message received!'
        data['type'] = 'message'
        self.write_message(data)
        q = self.application.settings.get('queue')
        q.put(message)


def main():
    tasks_queue = multiprocessing.Queue()
    results_queue = multiprocessing.Queue()

    parse_command_line()

    # here we define the routes that the web app handles
    app = Application(
        handlers=[
            (r"/index2.html", IndexHandler2),
            (r"/index.html", IndexHandler),
            (r"/grid.html", GridHandler),
            (r"/bars.html", BarsHandler),
            (r"/distance.html", DistanceHandler),
            (r"/dust.html", DustHandler),
            (r"/temperature.html", TempHandler),
            (r"/temperature_qual.html", TempQHandler),
            (r"/rh.html", RhHandler),
            (r"/co2.html", CO2Handler),
            (r"/co2_qual.html", CO2qualHandler),
            (r"/ws", MetricsHandler)
        ],
        cookie_secret="__air_1__",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=options.debug,
        queue=tasks_queue
    )

    # listen to the port and start the app loop and wait for clients
    server = HTTPServer(app)
    server.listen(options.port)
    print("Listening on port:", options.port)

    def check_results():
        if not results_queue.empty():
            result = results_queue.get()
            # print("tornado received from agent: " + str(result))
            for c in clients:
                c.write_message(result)

    the_agent = Agent(tasks_queue, results_queue)
    the_agent.daemon = True
    scheduler = tornado.ioloop.PeriodicCallback(check_results, 500)
    scheduler.start()

    the_agent.start()
    io_loop = tornado.ioloop.IOLoop.current()
    try:
        io_loop.start()
    except KeyboardInterrupt:
        tasks_queue.close()
        results_queue.close()
        the_agent.close()
        scheduler.stop()
        io_loop.stop()
    print("Bye!")
    sys.exit(0)


if __name__ == '__main__':
    main()
