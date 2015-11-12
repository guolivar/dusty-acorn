# DUSTY Air quality CORNer

Data parsing and visualisation for the Children's Air Quality Learning Corner. The data comes from a PACMAN (https://bitbucket.org/guolivar/pacman/wiki/Home) and it is converted to web pages aimed at children.

## Running the app locally

You will need the following tools installed in order to run this app

- Python 2.7+
- Tornado (`pip install tornado`)
- pySerial (`pip install pyserial`)

It has been developed and tested on a Ubuntu 14.04 with Chrome 46+, on a Mac OS 10 with Chrome 46+ and on a RPi Raspbian Jessie with Midori 0.5.11+

Once you have cloned the repository locally, fire your terminal in the project directory, and start the system with `python run.py`. You can browse the app in your browser using the URL `http://localhost:8080`.

It will call the main method in the web_server.py script, which starts i) a Tornado web application with some handlers, a WebSocket server, two queues and a periodic callback (to check one of the queues), and ii) another "agent" thread.

The WebSocket server will communicate with the agent through its queues. One being for items to process, and other with responses. The response always contains a heartbeat object, which is a dictionary with various metrics to be displayed in the UI.

This app is based on tracker, another tool written in NIWA to monitor a device that controls hardware that tracks the sun, deployed in Lauder/NZ and Antarctica.

## Configurations

The bind address by default is set to `0.0.0.0` in the web_server.py file.

The port is set to `8080` in the web_server.py file.

The WebSocket URL used by the JavaScript code to connect to the server defaults to `ws://localhost:8080` and is defined in `templates/index.html`. You may need to change this address, in case you are trying to allow remote users to use your app.
