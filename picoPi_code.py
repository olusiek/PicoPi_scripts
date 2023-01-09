from machine import Pin
import utime
import network
import urequests as request
import json
#import time

machine.freq(240000000)

SSID = "SSID"
SSID_PSK = "SSID_PSK"

def ultraX(TRIG_PIN, ECHO_PIN, LED_PIN, ID, DEBUG=0):
        
    TRIG = Pin(TRIG_PIN, Pin.OUT)
    ECHO = Pin(ECHO_PIN, Pin.IN)
    
    LED = Pin(LED_PIN, Pin.OUT)
    
    LED.low()
    LED.high()
    
    TRIG.low()
    utime.sleep_us(2)
    TRIG.high()
    utime.sleep_us(5)
    TRIG.low()
    
    while ECHO.value() == 0:
        signaloff = utime.ticks_us()
        if (DEBUG == 1):
            print("SIGNALOFF (dla id = ", ID ,") = ", signaloff)
        
    while ECHO.value() == 1:
        signalon = utime.ticks_us()
        if (DEBUG == 1):
            print("SIGNALON (dla id = ", ID ,") = ", signalon)
    
    timepassed = signalon - signaloff
    if (DEBUG == 1):
        print("TIMEPASSED: ", timepassed)
    
    distance = (timepassed * 0.0343) /2
    if (DEBUG == 1):
        print("UltraX - The distance from object in meter ", ID , " is ", distance ,"cm")
    
    LED.low()
#    if (distance > 1300):
#        break
#    else:
    return distance

def send_data_https(DISTANCE,ID,DEBUG):
    if (DEBUG == 1):
        print("Dystans:", DISTANCE,". ID = ",ID)
        
    payload = "oczyszczalnia,sensor=us-015,sensor_id=" + str(ID) + ",location=oczyszczalnia distance=" + str(DISTANCE)
    if (DEBUG == 1):
        print("Payload: ",payload)
        
    res = request.request(method='POST',url='http://INFLUXDB_URL:PORT/write?db=DBNAME',data=payload,headers={'Content-Type': 'application/json'})
    
    if (DEBUG == 1):
        print(res.text)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID,SSID_PSK)

while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
    utime.sleep(1)

print(wlan.ifconfig())

headers = { 'Content-Type': 'application/json' }
URL = "http://INFLUXDB_URL:PORT"
DBNAME = 'DBNAME'


while True:

    distance = ultraX(3,2,7,1,0)
    print("Dystans: ", distance)
    send_data_https(round(distance),1,1)
    utime.sleep(20)
    distance = ultraX(15,14,6,2,0)
    print("Dystans2: ",distance)
    send_data_https(round(distance),2,1)
    utime.sleep(20)
#    print("Status WiFI ", SSID ,":",wlan.ifconfig())
    
    
