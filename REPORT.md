# Complications Report: Remote Control of Temperature and Humidity with Raspberry Pi Pico W 
## Executive Summary:
The goal of this project is to remotely monitor and control temperature and humidity levels using a Raspberry Pi Pico W, DHT11 sensor, and the Adafruit IO platform. This report provides a revised perspective on the challenges faced, including hardware issues such as a previously broken DHT11 sensor. It outlines these challenges and proposes mitigations.

## Challenges and Mitigations:
### Hardware Compatibility and Reliability:
Challenge: Ensuring compatibility between the Raspberry Pi Pico W and the sensor. An additional complication was that a previous DHT11 sensor broke due to incorrect wiring.
Mitigation: Use well-documented and verified wiring guides. The broken DHT11 sensor had to be replaced, necessitating added caution moving forward.

### Code Organization and Security:
Challenge: Storing sensitive environmental variables securely.
Mitigation: Use a dedicated config file to securely store environment variables like WiFi SSID and password.

### Network Connectivity:
Challenge: Unreliable network connectivity can result in data loss or control issues.
Mitigation: A WiFi Manager class handles WiFi connection and logs the connection status.

### MQTT Subscription:
Challenge: Ensuring continuous device subscription to MQTT topics for real-time updates.
Mitigation: The script has undergone refactoring, incorporating try-except blocks at multiple points to gracefully catch and manage exceptions. ***(This was encountered during the [video presentation](https://youtu.be/Elspm2BnogU?t=140) when the On and Off buttons were unresponsive due to a non-functional broker.)***

### LED Control:
Challenge: The built-in LED was not activating as expected, which affects the remote status indication.
Mitigation: Verify GPIO pin configuration and the callback methods that trigger the LED.

### Exception Handling:
Challenge: Several parts of the program are prone to exceptions, such as MQTT message checking, sensor data gathering, and data publishing.
Mitigation: Exception handling is catching and logging exceptions at each critical step.

### Data Integrity:
Challenge: Incomplete or incorrect data may be published to Adafruit IO.
Mitigation: Data is only published if there are no exceptions during reading from the sensor.

### Security:
Challenge: Safeguarding sensitive data like connection IDs and Wi-Fi information.
Mitigation: Sensitive environmental variables are stored securely in a dedicated configuration file.

### Code Complexity:
Challenge: As features are added, the code could become complex.
Mitigation: Apply Object-Oriented Programming (OOP) principles to keep the codebase modular and readable.


## Conclusion:
Learning from past hardware failures, like the broken DHT11 sensor, is crucial for the successful remote monitoring and control of temperature and humidity. This careful approach will ensure the system's functionality and reliability through the Raspberry Pi Pico W and the Adafruit IO platform.

[Video link ](https://www.youtube.com/watch?v=Elspm2BnogU)
