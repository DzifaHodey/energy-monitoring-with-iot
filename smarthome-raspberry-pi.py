import threading
import datetime
import RPi.GPIO as GPIO
import time
import spidev
import http.client
import json

spi = spidev.SpiDev() # Created an object
spi.open(0,0)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

TRIG = 4
ECHO = 17
DOOR_BUZZER = 26 #SG2 in schematic
LDR = 5
EXT_LED = 25 #LED1 in schematic
FLAME_CHANNEL = 12
HALL_PIR = 23
HALL_LED = 16 #LED3 in schematic
KITCHEN_PIR = 7
KITCHEN_LED = 20
FLAME_CHANNEL = 21
FIRE_ALARM = 19
FAN = 22

GPIO.setup(FAN, GPIO.OUT)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(DOOR_BUZZER,GPIO.OUT)
GPIO.setup(EXT_LED,GPIO.OUT)
GPIO.setup(FLAME_CHANNEL, GPIO.IN)
GPIO.setup(HALL_PIR, GPIO.IN) #HALL_PIR
GPIO.setup(HALL_LED, GPIO.OUT) #HALL_LED
GPIO.setup(KITCHEN_PIR, GPIO.IN) 
GPIO.setup(KITCHEN_LED, GPIO.OUT)
GPIO.setup(FIRE_ALARM, GPIO.OUT) #HALL_LED
start=time.perf_counter()

motion = 0
motion1 = 0
dist =[]
tempp = []
brightness = []
flame_val = 0
fire_alarmv = 0
fan_val = 0
hall_light = 0
kitchen_light = 0
doorbell = 0
extlight = 0
current_mode = 'undefined'

def ultrasonic():
    global doorbell
    GPIO.output(TRIG, False)
    time.sleep(0.00001)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
      pulse_start = time.time()
    while GPIO.input(ECHO)==1:
      pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance+1.15, 2)
    dist.append(distance)
#    print(dist)
    if distance >1 and distance <50:
        print ("Alert: Person at entrance")
        GPIO.output(DOOR_BUZZER,True)
        doorbell+=1
        time.sleep(1)
        GPIO.output(DOOR_BUZZER,False)
        time.sleep(1) 
    else:
        GPIO.output(DOOR_BUZZER,False)
    time.sleep(0.1)
    return doorbell
      
def averages(dist, brightness,tempp):
    sum_dist = 0
    sum_brightness = 0
    sum_tempp = 0
    for d in dist:
        sum_dist = sum_dist + d
    for b in brightness:
        sum_brightness += b
    for t in tempp:
        sum_tempp += t

    avg_distance = round((sum_dist / len(dist)),2)
    avg_brightness = round((sum_brightness / len(brightness)),2)
    avg_tempp = round((sum_tempp / len(tempp)),2)
    return avg_distance, avg_brightness, avg_tempp;
    


def ldr_val(LDR):
    global extlight
    count = 0
    GPIO.setup(LDR, GPIO.OUT)
    GPIO.output(LDR, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(LDR, GPIO.IN)
    while (GPIO.input(LDR) == GPIO.LOW):
        count += 1
    brightness.append(count)
    print("LDR", count)
    if count >40:
        print ('It is dark. Exterior light is turned on.')
        GPIO.output(EXT_LED, True)
        extlight +=1
    else:
        GPIO.output(EXT_LED, False)
    return extlight


def hall_occupancy():
    global motion
    global hall_light
#    time.sleep(2) # to stabilize sensor
    if GPIO.input(HALL_PIR):
        motion += 1
        GPIO.output(HALL_LED, False)
        hall_light += 1
#        time.sleep(1) #to avoid multiple detection
        print("Hall Motion Detected...")    
    else:
        GPIO.output(HALL_LED, True)
#        motion =0
    return motion, hall_light
#    time.sleep(0.0000001) #loop delay, should be less than detection delay

def kitchen_occupancy():
    global motion1
    global kitchen_light
#    time.sleep(2) # to stabilize sensor
    if GPIO.input(KITCHEN_PIR):
        motion1 += 1
        GPIO.output(KITCHEN_LED, False)
        kitchen_light +=1
        time.sleep(2) #to avoid multiple detection
        print("Kitchen Motion Detected...")    
    else:
        GPIO.output(KITCHEN_LED, True)
    return motion1, kitchen_light
#    time.sleep(0.1)


def analogInput(channel):
  spi.max_speed_hz = 1350000
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

def temp():
    global fan_val
    temp_value = analogInput(0)
    volts = (temp_value * 3.3) / 1024
    temperature = volts / (10.0 / 1000)
    print ("%4d/1023 => %5.3f V => %4.1f °C" % (temp_value, volts,
            temperature))
    tempp.append(temperature)
    time.sleep(0.5)
    if temperature >=30:
        GPIO.output(FAN,False)
        fan_val +=1
    else:
        GPIO.output(FAN,True)
        fan_val = 0
    return fan_val    
    

def current_fan():
    current_value = 0
    loadname = 'hall_fan'
    loadlocation = 'hall'   
    for x in range(20):
        current_value += analogInput(1)
    current_value = current_value/20
    volt = (4.89*current_value)/1000
    actual_volt = 2.5 - volt
    current = actual_volt * 10
    power = actual_volt * current * 0.0025
#    print ("%4d/1023 => %5.3f V => %4.1f A => %4.1f W" % (current_value, actual_volt,
#            current, power))
    return loadname, loadlocation, round(actual_volt,2), round(current,2),round(power,2)


def current_hl():
    current_value = 0
    loadname = 'hall_light'
    loadlocation = 'hall'   
    for x in range(20):
        current_value += analogInput(2)
    current_value = current_value/20
    volt = (4.89*current_value)/1000
    actual_volt = 2.5 - volt
    current = actual_volt * 10
    power = actual_volt * current
#    print ("%4d/1023 => %5.3f V => %4.1f A => %4.1f W" % (current_value, actual_volt,
#            current, power))
    return loadname, loadlocation, round(actual_volt,2), round(current,2),round(power,2)

 
def flame():
    global flame_val
    global fire_alarmv
    if GPIO.input(FLAME_CHANNEL):
        flame_val +=1
        GPIO.output(FIRE_ALARM,True)
        fire_alarmv +=1
        print("flame detected")
    else:
        GPIO.output(FIRE_ALARM,False)
    return flame_val,fire_alarmv


def addsensordata():
    avg_dist, avg_bright, avg_temp = averages(dist,brightness,tempp)
    flamev = flame()[0]
    motion_hval = hall_occupancy()[0]
    motion_kval = kitchen_occupancy()[0]
#    print("motion",motion_val)
    post_sensor = http.client.HTTPConnection('127.0.0.1:5000')
    headers = {'Content-type': 'application/json'}
    sensor_data = {
        "hall_temperature" : avg_temp,
        "hall_motion" : motion_hval,
        "kitchen_motion" : motion_kval,
        "kitchen_firestatus" : flamev,
        "external_brightness" : avg_bright,
        "door_distance" : avg_dist,
        "user_id" : "1"
    }
    json_data = json.dumps(sensor_data)
    post_sensor.request('POST', '/sensor', json_data, headers)
    response = post_sensor.getresponse()
    print(response.read().decode())
    dist.clear()
    brightness.clear()
    tempp.clear()
    motion = 0
    motion1 = 0
    flamev = 0
  
def addactuatordata():
    fanvalue = temp()
    hall_lightv = hall_occupancy()[1]
    kitchen_lightv = kitchen_occupancy()[1]
    falarm = flame()[1]
    doorbellv = ultrasonic()
    extlightv = ldr_val(LDR)
    post_actuator = http.client.HTTPConnection('127.0.0.1:5000')
    headers = {'Content-type': 'application/json'}
    actuator_data = {
        "hall_fan" : fanvalue,
        "hall_light" : hall_lightv,
        "kitchen_light" : kitchen_lightv,
        "kitchen_buzzer" : falarm,
        "kitchen_blender" :"1",
        "kitchen_stove" : "0",
        "external_light" : extlightv,
        "door_buzzer" : doorbellv,
        "state" : "automatic",
        "user_id" : "1"
    }
    json_data = json.dumps(actuator_data)
    post_actuator.request('POST', '/actuator', json_data, headers)
    response = post_actuator.getresponse()
    print(response.read().decode())
    fan_val = 0
    hall_light = 0
    kitchen_light = 0
    extlight = 0
    doorbell = 0
    
def addconsumption():
    load_name, load_location, load_voltage, load_current, load_power = current_fan()
    post_consumption = http.client.HTTPConnection('127.0.0.1:5000')
    headers = {'Content-type': 'application/json'}
    consumption_data = {
        "load_name" : load_name,
        "load_location" : load_location,
        "load_voltage" : load_voltage,
        "load_current" : load_current,
        "load_power" : load_power,
        "user_id" : "1"
    }
    json_data = json.dumps(consumption_data)
    post_consumption.request('POST', '/consumption', json_data, headers)
    response = post_consumption.getresponse()
    print(response.read().decode())

def manualControl(pin,state):
    Pin = globals()[pin]
    State = str(state).lower() in ("yes", "true", "t", "1")
    GPIO.output(Pin,State)

class controls:
    pinName = "none"
    pinMode = "null"


try:
    time.sleep(5)
    # Main loop
    while True:
        
        halloccupancy = threading.Thread(target=hall_occupancy, name='halloccupancy')
        kitchoccupancy = threading.Thread(target=kitchen_occupancy, name='kitchoccupancy')
        ldr = threading.Thread(target=ldr_val, name='ldr', args=(LDR,))
        Ultrasonic = threading.Thread(target=ultrasonic, name='Ultrasonic')
        Temp = threading.Thread(target=temp, name='Temp')
        fan_con = threading.Thread(target=current_fan, name='fan_con')
        hl_con = threading.Thread(target=current_hl, name='hl_con')
        sensordata = threading.Thread(target=addsensordata, name='sensordata')
        actuatordata = threading.Thread(target=addactuatordata, name='actuatordata')
        consumption = threading.Thread(target=addconsumption, name='consumption')
        finish = time.perf_counter()
        dur = round(finish-start)
        
        current_mode = http.client.HTTPConnection("127.0.0.1:5000")
        current_mode.request("GET", "/controlmode")
        Cresponse = current_mode.getresponse()
        mode = Cresponse.read().decode()
#        print(mode)
        if mode=="automatic":
            halloccupancy.start()
            ldr.start()
#            Ultrasonic.start()
            Temp.start()
            fan_con.start()
            kitchoccupancy.start()
            
            ldr.join()
#            Ultrasonic.join()
            Temp.join()
            fan_con.join()

            
            print('Duration:', (dur))
            if dur%100 == 0:
                sensordata.start()
                actuatordata.start()
                sensordata.join()
                actuatordata.join()              
            if dur%100 == 0:
               consumption.start()
               consumption.join()
               time.sleep(1)
            
        elif mode=="manual":
            controldata = http.client.HTTPConnection("127.0.0.1:5000")
            controldata.request("GET", "/controls")
            controlresp = controldata.getresponse()
            ctrldata =controlresp.read().decode()
            ctrls = json.loads(ctrldata)
            pinName1 = ctrls['pinName']
            pinMode1 = ctrls['pinMode']
#            print("New: ", pinMode1, pinName1)
            if (pinName1 != controls.pinName) or (pinMode1 != controls.pinMode):
                controls.pinName = pinName1
                controls.pinMode = pinMode1
                manualControl(pinName1, pinMode1)

            fan_con.start()
            hl_con.start()
            fan_con.join()
            hl_con.join()
            print('Duration:', (dur))              
            if dur%100 == 0:
               consumption.start()
               consumption.join()
               time.sleep(1)
            
            
        
       
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
