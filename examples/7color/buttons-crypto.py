#!/usr/bin/env python3

import signal
import RPi.GPIO as GPIO
import subprocess
import requests
from requests.exceptions import HTTPError
import json
import random
from decimal import *
import time

class Crypto:
    
    def __init__(self):
        self.btcUrl = "https://api.coinbase.com/v2/prices/spot?currency=EUR"
        self.ltcUrl = "https://api.coinbase.com/v2/prices/LTC-EUR/spot?currency=EUR"
        self.ethUrl = "https://api.coinbase.com/v2/prices/ETH-EUR/spot?currency=EUR"
        
    def getPrice(self, url):
            response = requests.get(url)
            response.raise_for_status()
            jsonResponse = response.json()
            return Decimal(jsonResponse.get("data").get("amount"))

    
    def next(self, buttonLabel=None):

        btc = ""
        ltc = ""
        eth = ""
        try:
            btc = round(self.getPrice(self.btcUrl), 0)
            ltc = self.getPrice(self.ltcUrl)
            eth = self.getPrice(self.ethUrl)
            ltcBtc = round(ltc/btc, 5)
            ethBtc = round(eth/btc, 4)
            
            
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
    
        imageNum = random.randint(1, 19)
        return {"image": "/home/pi/Pictures/image{}.jpg".format(imageNum), "line2": "BTC:{}e|LTC:{}|eth:{}".format(btc, ltcBtc, ethBtc)}

        
print("""buttons-crypto.py - A simple button tool for display a random image and the current crypto price.

Press Ctrl+C to exit!

""")

# Gpio pins for each button (from top to bottom)
BUTTONS = [5, 6, 16, 24]

# These correspond to buttons A, B, C and D respectively
LABELS = [1, 2, 3, 4]

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

crypto = Crypto()
                    
# "handle_button" will be called every time a button is pressed
# It receives one argument: the associated input pin.
def handle_button(pin):
    label = LABELS[BUTTONS.index(pin)]
    print("Button press detected on pin: {} label: {}".format(pin, label))
    if label == 4:
        subprocess.run(["sudo", "shutdown"])
    else:
        response = crypto.next(label)
        subprocess.run(["./html/html-image.sh", "./html/image-template.html", response.get("line1", ""), response.get("line2", ""), response.get("topRight", ""), response.get("image", "")])

# Loop through out buttons and attach the "handle_button" function to each
# We're watching the "FALLING" edge (transition from 3.3V to Ground) and
# picking a generous bouncetime of 250ms to smooth out button presses.
for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=250)

# Finally, since button handlers don't require a "while True" loop,
# we pause the script to prevent it exiting immediately.
#signal.pause()
signals = range(1, signal.NSIG)
while(True):
    handle_button(5)
    time.sleep(21600) # 6 hours
