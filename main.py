# main.py
import config  # Ensure you have a config.py file with WIFI_SSID and WIFI_PASSWORD
from WifiManager import WifiManager
from Sensor import Sensor
import time

def main():
    wifi_manager = WifiManager(config.WIFI_SSID, config.WIFI_PASSWORD)
    sensor = Sensor()
    
    try:
        wifi_manager.connect()
        # WiFi connected, keep the WiFi LED on
        wifi_manager.led.value(1)
        
        # Read sensor data in a loop
        while True:
            temp, hum = sensor.read()
            if temp is not None and hum is not None:
                print('Temperature: {:.1f} C'.format(temp))
                print('Humidity: {:.1f} %'.format(hum))
            else:
                print('Failed to read from the sensor')
            time.sleep(2)  # Wait for 2 seconds before reading again

    except RuntimeError as e:
        print(e)
        # WiFi not connected, WiFi LED remains off
        while True:
            wifi_manager.blink_led()

# Run main function
if __name__ == "__main__":
    main()
