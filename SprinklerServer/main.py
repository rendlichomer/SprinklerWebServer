from flask import Flask, render_template, url_for, redirect, request
from flask_mqtt import Mqtt
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from handle_config import readFile, getConfig, writeFile
import json

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'boroker.com' # Set broker url
app.config['MQTT_BROKER_PORT'] = 1883 # Set broker port
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False # Enable/Disable TLS
CONFIG = "config.json" # Config file path

mqtt = Mqtt()
topic = "Sprinklers" # Set MQTT topic

valves = readFile(CONFIG) # read config using handle_config

scheduler = BackgroundScheduler() # Intialize scheduler

# Define home page
@app.route("/")
def home():
    return render_template("home.html", valves = valves)

# Define config editor page
@app.route("/config", methods=['GET', 'POST'])
def config():
    global valves
    if request.method == "POST":
        valves = json.loads(request.form["config"]) # Recieve config editor data
        writeFile(CONFIG, valves) # overwrite config
    return render_template("config.html", json = getConfig(CONFIG))

# Define valve toggle endpoint
@app.route("/<id>/<action>")
def toggle(id, action, timer=False):
    global valves
    valves[int(id) - 1]["status"] = action
    writeFile(CONFIG, valves)
    mqtt.publish(topic, action) # Publish ON/OFF command
    if timer: # After job has finished create the next one
        scheduler.add_job(func=toggle(id, "ON"), trigger="interval", seconds=get_delay(valves[int(id) - 1]["time"]))
        scheduler.add_job(func=toggle(id, "OFF"), trigger="interval", seconds=get_delay(valves[int(id) - 1]["time"], 10))
    return redirect("/")

# Define MQTT client action on connection to broker
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe(topic) # Subscribe to topic

# Get the time between now and the scheduled time in seconds
def get_delay(hour, minute=0):
    current_date = datetime.today()
    required_date = current_date.replace(day=current_date.day, hour=hour, minute=minute, second=0, microsecond=0) + timedelta(days=1)
    time_delta = required_date - current_date
    return time_delta.total_seconds()

# Schedule watering for all valves
def schedule_watering(valves):
    try:
        for valve in valves:
            scheduler.add_job(func=toggle(valve["id"], "ON"), trigger="interval", seconds=get_delay(valve["time"]))
            scheduler.add_job(func=toggle(valve["id"], "OFF"), trigger="interval", seconds=get_delay(valve["time"], 10))
    except:
        None

schedule_watering(valves)
scheduler.start() # Start scheduler

if __name__ == "__main__":
    app.run(port="8080", debug=True)