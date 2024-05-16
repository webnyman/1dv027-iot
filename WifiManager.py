import network
import time
import config
from machine import Pin

class WifiManager:
    def __init__(self, led_pin=15):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.led = Pin(led_pin, Pin.OUT)

    def connect(self):
        self.wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
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

# Example usage
def main():
    wifi_manager = WifiManager()
    try:
        wifi_manager.connect()
        # WiFi connected, keep the LED on
        wifi_manager.led.value(1)
    except RuntimeError as e:
        print(e)
        # WiFi not connected, blink the LED
        while True:
            wifi_manager.blink_led()

# Run main function
if __name__ == "__main__":
    main()
