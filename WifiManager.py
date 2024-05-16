# wifi_manager.py
import network
import time
from machine import Pin

class WifiManager:
    def __init__(self, ssid, password, led_pin=11):
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.led = Pin(led_pin, Pin.OUT)
        self.led.value(0)  # Ensure LED is off initially

    def connect(self):
        self.wlan.connect(self.ssid, self.password)
        print(self.wlan.isconnected())

        wait = 10
        while wait > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            wait -= 1
            print('waiting for connection...')
            self.blink_led()
            time.sleep(1)

        if self.wlan.status() != 3:
            self.led.value(0)  # Turn off LED
            raise RuntimeError('wifi connection failed')
        else:
            self.led.value(1)  # Turn on LED
            print('connected')
            ip = self.wlan.ifconfig()[0]
            print('network config: ', ip)
            return ip

    def blink_led(self):
        self.led.value(1)  # LED ON
        time.sleep(0.5)
        self.led.value(0)  # LED OFF
        time.sleep(0.5)
