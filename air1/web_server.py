#!/usr/bin/env python

import os
import sys
import time
# Tornardo... HTTP, WebSockets, Events... - pip install tornado
import tornado.web # pip install tornado
import tornado.websocket
from tornado.httpserver import HTTPServer
from tornado.options import define, options, parse_command_line
# for queues
import multiprocessing
# for the agent
import agent

define("port", default=8080, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")

# Base class, you can add any logic common to all handlers
class BaseHandler(object):
    pass

# A handler for Web
class WebHandler(BaseHandler, tornado.web.RequestHandler):
    pass

# A web socket handler
class WebSocketHandler(BaseHandler, tornado.websocket.WebSocketHandler):
    pass

# The implementations. These are the actual handlers, that take care to respond users, 
# based on the routes that you create for the application.

# /index.html
class IndexHandler(WebHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("index.html", app_name='Air 1')

# /index2.html
class IndexHandler2(WebHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("index2.html", app_name='Air 1')


# /grid.html
class GridHandler(WebHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("grid.html", app_name='Air 1')

# /bars.html
class BarsHandler(WebHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("bars.html", app_name='Air 1')

# /distance.html
class DistanceHandler(WebHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("distance.html", app_name='Air 1')
        
# /dust.html
class DustHandler(WebHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("dust.html", app_name='Air 1')

# /temperature.html
class TempHandler(WebHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("temperature.html", app_name='Air 1')

# /co2.html
class CO2Handler(WebHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("co2.html", app_name='Air 1')

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

################################ MAIN ################################


def main():
    taskQ = multiprocessing.Queue()
    resultQ = multiprocessing.Queue()

    parse_command_line()

    # here we define the routes that the web app handles
    app = tornado.web.Application(
        handlers = [
            (r"/index2.html", IndexHandler2),
            (r"/index.html", IndexHandler), 
            (r"/grid.html", GridHandler),
            (r"/bars.html", BarsHandler),  
            (r"/distance.html", DistanceHandler),
            (r"/dust.html", DustHandler),
            (r"/temperature.html", TempHandler),
            (r"/co2.html", CO2Handler),
            (r"/ws", MetricsHandler)
            ],
        cookie_secret="__air_1__",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=options.debug,
        queue=taskQ
        )

    # listen to the port and start the app loop and wait for clients
    server = HTTPServer(app)
    server.listen(options.port)
    print "Listening on port:", options.port

    def checkResults():
        if not resultQ.empty():
            result = resultQ.get()
            #print "tornado received from agent: " + str(result)
            for c in clients:
                c.write_message(result)

    theAgent = agent.Agent(taskQ, resultQ)
    theAgent.daemon = True
    mainLoop = tornado.ioloop.IOLoop.instance()
    scheduler = tornado.ioloop.PeriodicCallback(checkResults, 500, io_loop = mainLoop)
    scheduler.start()

    theAgent.start()
    try:
        mainLoop.start()
    except KeyboardInterrupt:
        taskQ.close()
        resultQ.close()
        theAgent.close()
        scheduler.stop()
        mainLoop.stop()
    print "Bye!"
    sys.exit(0)
