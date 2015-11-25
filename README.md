# DUSTY Air quality CORNer

Data parsing and visualisation for the Children's Air Quality Learning Corner. The data comes from a PACMAN (https://bitbucket.org/guolivar/pacman/wiki/Home) and it is converted to web pages aimed at children.

## Running the app locally

You will need the following tools installed in order to run this app

- Python 2.7+
- Tornado (`pip install tornado`)
- pySerial (`pip install pyserial`)

It has been developed and tested on a Ubuntu 14.04 with Chrome 46+, on a Mac OS 10 with Chrome 46+ and on a RPi Raspbian Jessie with Midori 0.5.11+

Once you have cloned the repository locally, fire your terminal in the project directory, and start the system with `python run.py`. You can browse the app in your browser using the URL `http://localhost:8080`.

Different web pages have been implemented to test different visualization methods:
* `http://localhost:8080/index.html` Basic "hello world" page showing the live feed from PACMAN as a table of values and as simple visualizations. Intended to illustrate the data and general visualization capabilities.
* `http://localhost:8080/bars.html` Vertical bars covering the screen, one for each sensor in different colours that reflect the measurements, taller bar means higher measurements.
The range of the bars is defined by the last 60 readings (max/min).
The distance sensor also controls the sounds emitted (think theremin).
* `http://localhost:8080/grid.html` The screen is divided in 4 sections dealing with specific sensors.
* `http://localhost:8080/temperature.html` The screen shows a single vertical bar scaled according to the last 60 readings (max/min) and if the max is reached, a chime plays.
* `http://localhost:8080/co2.html` The screen shows a single vertical bar scaled according to the last 60 readings (max/min) and if the max is reached, a chime plays.
* `http://localhost:8080/distance.html` The screen shows a single vertical bar scaled from 0 to ~60cm. The distance sensor also controls the sounds emitted (think theremin).
* `http://localhost:8080/dust.html` The screen shows a field of particles floating. The number of particles in the window is controlled by the readings of the dust sensor.
If the current reading is the max over the past 60 readings, a chime plays.

It will call the main method in the web_server.py script, which starts i) a Tornado web application with some handlers, a WebSocket server, two queues and a periodic callback (to check one of the queues), and ii) another "agent" thread.

The WebSocket server will communicate with the agent through its queues. One being for items to process, and other with responses. The response always contains a heartbeat object, which is a dictionary with various metrics to be displayed in the UI.

This app is based on tracker, another tool written in NIWA to monitor a device that controls hardware that tracks the sun, deployed in Lauder/NZ and Antarctica.

## Configurations

The bind address by default is set to `0.0.0.0` in the web_server.py file.

The port is set to `8080` in the web_server.py file.

The WebSocket URL used by the JavaScript code to connect to the server defaults to `ws://localhost:8080` and is defined in `templates/index.html`. You may need to change this address, in case you are trying to allow remote users to use your app.
