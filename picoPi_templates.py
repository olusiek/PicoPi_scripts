#some pico pi basics


#setting up the LED

import machine

led = machine.Pin("LED",machine.Pin.OUT)

led.on()
time.sleep(10)
led.off()
led.toggle()


# setting up the WiFi

import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('ssid', 'pass')

while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
    time.sleep(1)

print(wlan.ifconfig())


# 