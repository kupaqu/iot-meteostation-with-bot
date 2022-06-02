import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient
#from datetime import datetime

mongoc = MongoClient("localhost:27017")
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    global mongoc
    data = msg.payload.decode('ASCII').split("|")
    #now = datetime.now()
    #dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    if len(data) == 4:
        try:
            json_string = f'{{"time":"{data[0]}","temperature":{data[1]},"moisture":{data[2]},"pressure":{data[3]}}}'
            json_obj = json.loads(json_string)
            db = mongoc.meteodata
            db.timeseries.insert_one(json_obj)
            print(json_obj)
        except ValueError:
            print("Wrong format of message!")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.emqx.io", 1883, 60)

client.subscribe("isu/iot/meteo")

client.loop_forever()
