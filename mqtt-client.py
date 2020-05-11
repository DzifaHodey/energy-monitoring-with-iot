import paho.mqtt.client as mqtt
import time
import mysql.connector

MQTT_SERVER = "127.0.0.1"
MQTT_PATH = "IssueReport"

mydb = mysql.connector.connect(
  host="localhost",
  user="mqttclient",
  passwd="websockets",
  database="smart_home"
)

mycursor = mydb.cursor()
 
# The callback when conected.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc)) 
    client.subscribe(MQTT_PATH)
 
# Callback when message received
def on_message(client, userdata, msg):
    t1_start = time.perf_counter()
 #   print(msg.topic+" "+str(msg.payload))
    rep = msg.payload.decode('utf-8')
    print(msg.payload.decode('utf-8'))
#    print ("This listens to IssueReport")
    sql = "INSERT INTO reports(report, user_id) VALUES (%s, %s)"
    val = (rep, 1)
    mycursor.execute(sql, val)
    mydb.commit()
    t1_stop = time.perf_counter()
    print("Elapsed time:", t1_stop-t1_start)
    print(mycursor.rowcount, "record inserted.")
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)

client.loop_forever()

