#!/usr/bin/python

__author__ = "Batuhan AVLAYAN"

# You can reach dht11 library from here -> git clone https://github.com/szazo/DHT11_Python.git

import RPi.GPIO as GPIO
import time
import dht11
import requests 

API_KEY         = 'api key'
API_URL         = 'https://api.thingspeak.com/update'
SLEEP           = 1

def initialize_GPIO():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()

def get_data_from_raspberry():
    dht11_sensor = dht11.DHT11(pin=4)
    while True:
        result = dht11_sensor.read()
        if(result.is_valid()):
            temprature = result.temperature
            humidity = result.humidity
            print("Temperature: %d C" % temprature)
            print("Humidity: %d %%" % humidity)
            send_data_to_thingspeak(temprature, humidity)
        time.sleep(SLEEP)

def send_data_to_thingspeak(temprature, humidity):     
    data = {'api_key': API_KEY, 'field1':temprature, 'field2':humidity};
    result = requests.post(API_URL, params=data)
    print result.status_code
    if result.status_code == 200:
        print "Success!! Thingspeak"
    else:
        print "Fail!! Thingspeak"

if __name__ == "__main__":
    initialize_GPIO()
    get_data_from_raspberry()
