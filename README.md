# SprinklerWebServer
Flask web server that manages the sprinkler system (available in the SprinklerController repo)

* Server built with Python's Flask module, Jinja2 and the flask-mqtt module.
* Valves/Sprinklers are controlled via MQTT command either through the ui or through automated scheduler.
* Server serves a control panel view of the defined valves/sprinklers over port 8080.
* The amount of valves and the time they should be automatically turned on can be modified.
* Valve details and settings a read and written to/from configuration file.
* Configuration file can be edited via the ui at your_server_ip:8080/config.
