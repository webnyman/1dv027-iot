from machine import Pin
import time

# Configure the GPIO pin (GP15 in this example) for the LED
led = Pin(14, Pin.OUT)

def test_led():
    print("Turning LED on")
    led.value(1)  # Turn LED on
    time.sleep(1)  # Keep it on for 1 second
    print("Turning LED off")
    led.value(0)  # Turn LED off
    time.sleep(1)  # Keep it off for 1 second

# Test the LED
while True:
    test_led()
