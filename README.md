# ESP8266_temp_sensor
An ESP8266 running Micropython, connected to a DHT22, reporting temp and humidity via MQTT

This project borrows heavily from the [Fabian Affolter](https://home-assistant.io/blog/2016/08/31/esp8266-and-micropython-part2/) and [@davea](https://github.com/davea/sonoff-mqtt).

## Setup

### Create config.json

All the necessary configuration options are stored in a json file called `config.json`.  See `config.py` for available options.

### Install rshell

Rshell can copy files to the board over serial using a syntax much similar to the unix `cp` command.

```
pip3 install rshell
```

### Copy files to the board 

```
rshell -p /dev/ttyUSB0 -b 115200 --buffer-size=32 cp src/boot.py src/config.py src/main.py src/config.json /pyboard/
```
