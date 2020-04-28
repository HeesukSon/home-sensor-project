# home-sensor-project
In this project I wrote a python program which extracts sensor readings from wired Phidget sensors wireless Particle sensors. The sensor values are either printed as json objects or stored in timescale database. I used Raspberry pi 3 board as the base hardware to which Phidget sensors and hub device are attached. For fundamental understanding of the hardware setup, you may want to read <a href="https://medium.com/@heesuk.chad.son/diy-iot-project-in-python-raspberry-pi-phidget-sensor-7c3c8965a817">my Medium story</a>. I mentioned only a Phidget sound sensor in the story. However, I used addtional Phidget sensors in this project: Temperature, Humidity, and Precision Light. 

As Phidget platform has evolved, its hardware and software classes have been also evolved, which entails annoying programming library incompatibility issues. Especially, in Phidget22 library, sensor modules fall into different classes such as SoundSensor, VoltageRatioInput, and VoltageInput. This separation is due to the hardware evolution and can confuse developers a lot. Especially, Phidget does not provide enough samples to Python programmers.

The development of and integration with particle platform will be written as a Medium post in near future.

I hope this simple code sample can provide python-based makers with helpful intuition. To exclude any concerns about the external libraries and virtual environment, I did not uploaded the required modules imported in the code sample. So they must be downloaded or installed accordingly to your development environment setup. 

## Notes on Execution
In this project, the client has platform-specific dependencies on Phidgets and Python. Since the Phidgets library requires sudo access permission, you need to type the command below to run the client code:
```sudo path-to-the-python3-binary path-to-the-client-python-program```

## Branch description
* **master** branch is equivalent to **local-print** branch. With these two branches, you can try printing out Phidget sensor data in a local terminal. 
* As an advanced branch, you can try **server-client**. In this branch, the Raspberry pi to which Phidget sensors are attached turns into a sensor client which sends the sensor data to a server via a TCP connection. 
* **server-client-timescaledb** branch is an extension of the **server-client** branch. In this branch, the server stores the transmitted sensor data to a **timescale database**, which is a widely used database to store timeseries data stream.
* **server-multithread** branch extends **server-client-timescaledb** branch so that it can support multiple connections from more than one sensor client.
