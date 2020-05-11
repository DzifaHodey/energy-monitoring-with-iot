from datetime import datetime, date, time
from flask import Flask, request, jsonify, Blueprint, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user, logout_user, login_required

from werkzeug.security import generate_password_hash, check_password_hash

# #Init App
app = Flask(__name__)
CORS(app)
app.secret_key = 'theoldbrownfox123'

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://raspberrypi:root@192.168.137.1:3306/smart_home'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
#init marshmallow
ma = Marshmallow(app)


@login_manager.user_loader
def load_user(user_id):
  return Users.query.get(int(user_id))

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login_post():
    data = request.get_json()
    email_address = data['email_address']
    pass_word = data['pass_word']
    
    # remember = True if request.form.get('remember') else False
    user = Users.query.filter_by(email_address=email_address).first()
    user.pass_word=generate_password_hash(pass_word)

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.pass_word, pass_word):
#        flash('Please check your login details and try again.')
        return 'unauthorized' # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    # login_user(user, remember=remember)
    return 'authorized'


app.register_blueprint(auth)



####################### MODELS ###################
# create table
class Users(UserMixin,db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    pass_word = db.Column(db.String)
    email_address = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    access_code = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())
#    sensor_device = db.relationship('sensor_data', backref= 'sensor_d', lazy=True)
#    actuator_device = db.relationship('actuator_data', backref= 'actuator_d', lazy=True)

    def set_password(self, pass_word):
        self.pass_word = generate_password_hash(pass_word)
    
    
class Sensor_data(db.Model):
    sensor_id = db.Column(db.Integer, primary_key=True)
    hall_temperature = db.Column(db.Float, nullable=False)
    hall_motion = db.Column(db.Integer, nullable=False)
    kitchen_motion = db.Column(db.Integer, nullable=False)
    kitchen_firestatus = db.Column(db.Integer, nullable=False)
    external_brightness = db.Column(db.Float, nullable=False)
    door_distance = db.Column(db.Float, nullable=False)
    date_read = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    def __init__(self, hall_temperature, hall_motion, kitchen_motion, kitchen_firestatus,external_brightness,door_distance, date_read, user_id):
        self.hall_temperature = hall_temperature
        self.hall_motion = hall_motion
        self.kitchen_motion = kitchen_motion
        self.kitchen_firestatus = kitchen_firestatus
        self.external_brightness = external_brightness
        self.door_distance = door_distance
        self.date_read = date_read
        self.user_id = user_id
    
class Actuator_data(db.Model):
    actuator_id = db.Column(db.Integer, primary_key=True)
    hall_light = db.Column(db.Integer, nullable=False)
    hall_fan = db.Column(db.Integer, nullable=False)
    kitchen_light = db.Column(db.Integer, nullable=False)
    kitchen_buzzer = db.Column(db.Integer, nullable=False)
    kitchen_blender = db.Column(db.Integer, nullable=False)
    kitchen_stove = db.Column(db.Integer, nullable=False)
    external_light = db.Column(db.Integer, nullable=False)
    door_buzzer = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(10), nullable=False)
    date_read = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),nullable=False)

    def __init__(self, hall_light, hall_fan, kitchen_blender, kitchen_light, kitchen_buzzer, kitchen_stove, external_light, door_buzzer, state, date_read, user_id):
        self.hall_fan = hall_fan
        self.hall_light = hall_light
        self.kitchen_blender = kitchen_blender
        self.kitchen_buzzer = kitchen_buzzer
        self.kitchen_light = kitchen_light
        self.kitchen_stove = kitchen_stove
        self.external_light=external_light
        self.door_buzzer = door_buzzer
        self.state = state
        self.date_read = date_read
        self.user_id = user_id


class Consumption(db.Model):
    consumption_id = db.Column(db.Integer, primary_key=True)
    load_name = db.Column(db.String, nullable=False)
    load_voltage = db.Column(db.Float, nullable=False)
    load_current = db.Column(db.Float, nullable=False)
    load_power = db.Column(db.Float, nullable=False)
    load_location = db.Column(db.String, nullable=False)
    date_read = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    def __init__(self, load_name, load_location, date_read, user_id, load_voltage, load_current, load_power):
        self.load_name = load_name
        self.load_location = load_location
        self.date_read = date_read
        self.user_id = user_id
        self.load_current = load_current
        self.load_voltage = load_voltage
        self.load_power = load_power


class Reports(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    report = db.Column(db.String, nullable=False)
    date_sent = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    def __init__(self, report, date_sent, user_id):
        self.report = report
        self.date_sent = date_sent
        self.user_id = user_id

# #################################################################
# #API FUNCTIONS 
#main

main = Blueprint('main', __name__)

app.register_blueprint(main)
# ############## CONSUMPTION ##########################

# #GET ALL CONSUMPTION DATA
@app.route('/consumption', methods=['GET'])
def get_allconsumption():
    cons = Consumption.query.all()
    output = []
    for con in cons:
        con_data = {}
        con_data['load_name'] = con.load_name
        con_data['load_location'] = con.load_location
        con_data['date_read'] = con.date_read
        con_data['load_voltage'] = con.load_voltage
        con_data['load_current'] = con.load_current
        con_data['load_power'] = con.load_power
        output.append(con_data)
    return jsonify({'consumptions' : output})

# #GET CONSUMPTION TABLE
@app.route('/consumption/table', methods=['GET'])
def get_consumptiontable():
    cons = Consumption.query.all()
    output = []
    for con in cons:
        con_data = {}
        con_data['load_name'] = con.load_name
        con_data['load_location'] = con.load_location
        con_data['date_read'] = con.date_read
        con_data['load_voltage'] = con.load_voltage
        con_data['load_current'] = con.load_current
        con_data['load_power'] = con.load_power
        output.append(con_data)
    return jsonify({'consumptions' : output})



#GET CONSUMPTION DATA BY LOAD NAME
@app.route('/consumption/<load_name>', methods=['GET'])
def get_consumptionbyname(load_name):
    load_name = "%" + load_name + "%"
    cons = Consumption.query.filter(Consumption.load_name.like(load_name)).all()
    output =[]
    if not cons:
        return jsonify({'message' : 'device not found'})
    for con in cons:
        con_data = {}
        con_data['load_name'] = con.load_name
        con_data['load_location'] = con.load_location
        con_data['date_read'] = con.date_read
        con_data['load_voltage'] = con.load_voltage
        con_data['load_current'] = con.load_current
        con_data['load_power'] = con.load_power
        output.append(con_data)
    return jsonify({'consumption' : output})



#GET CONSUMPTION DATA BY LOAD LOCATION
@app.route('/consumption/location/<load_location>', methods=['GET'])
def get_consumptionbyloc(load_location):
    load_location = "%" + load_location + "%"
    cons = Consumption.query.filter(Consumption.load_location.like(load_location)).all()
    output = []
    if not cons:
        return jsonify({'message' : 'Location not found'})
    for con in cons:
        con_data = {}
        con_data['load_name'] = con.load_name
        con_data['load_location'] = con.load_location
        con_data['date_read'] = con.date_read
        con_data['load_voltage'] = con.load_voltage
        con_data['load_current'] = con.load_current
        con_data['load_power'] = con.load_power
        output.append(con_data)
    return jsonify({'consumption' : output})


#GET CONSUMPTION DATA BY DATE RECORDED
@app.route('/consumption/date/<date_read>', methods=['GET'])
def get_consumptionbydate(date_read):
    date_read = "%" + date_read + "%"
    cons = Consumption.query.filter(Consumption.date_read.like(date_read)).all()
    output = []
    if not cons:
        return jsonify({'message' : 'No data on such date'})
    for con in cons:
        con_data = {}
        con_data['load_name'] = con.load_name
        con_data['load_location'] = con.load_location
        con_data['date_read'] = con.date_read
        con_data['load_voltage'] = con.load_voltage
        con_data['load_current'] = con.load_current
        con_data['load_power'] = con.load_power
        output.append(con_data)
    return jsonify({'consumption' : output})


#ADD CONSUMPTION DATA
@app.route ('/consumption', methods =['POST'])
def add_consumption():
    data = request.get_json()
    new_consumption = Consumption(load_name = data['load_name'], load_location = data['load_location'], load_voltage = data['load_voltage'], load_current = data['load_current'], load_power = data['load_power'], user_id = data['user_id'], date_read = datetime.now())
    db.session.add(new_consumption)
    db.session.commit()
    return jsonify({'message': 'New consumption log added'}) 


# #GET CONSUMPTION TOTAL FOR CHART
@app.route('/consumption/total/<date_read>/<limit>', methods=['GET'])
def totalConsumption(date_read, limit):
    date_read = "%" + date_read + "%"
    cons = Consumption.query.filter(Consumption.date_read.like(date_read)).all()
    power = 0
    for con in cons:
        power += con.load_power
    unused = abs(int(limit) - power)
    data = {'Consumption per Month': 'Value','Consumed' : power, 'Unused' : unused}
    return data
   
# #GET DAILY CONSUMPTION DATA FOR CHART
@app.route('/consumption/daily/<date_read>', methods=['GET'])
def dailyconsumption(date_read):
    date_read = "%" + date_read + "%"
    cons = Consumption.query.filter(Consumption.date_read.like(date_read)).all()
    output = []
    hl = 0
    kl = 0
    hf = 0
    el = 0
    stove = 0
    coffee = 0
    for con in cons:
        con_data = {}
        con_data['load_name'] = con.load_name
        con_data['load_power'] = con.load_power
        output.append(con_data)
    for outdata in output:
        if outdata['load_name'] == "hall_light":
            hl += outdata['load_power']
        elif outdata['load_name'] == "hall_fan":
            hf += outdata['load_power']
        elif outdata['load_name'] == "kitchen_light":
            kl += outdata['load_power']
        elif outdata['load_name'] == "stove":
            stove += outdata['load_power']
        elif outdata['load_name'] == "coffee_maker":
            coffee += outdata['load_power']
        elif outdata['load_name'] == "external_light":
            el += outdata['load_power']
    data = {'Device':'Daily Consumption',
    'Hall Light' : hl,
    'Hall Fan' : hf,
    'Kitchen Light':kl,
    'Exterior Light' : el,
    'Stove': stove,
    'Coffee Maker': coffee}
    return data



################ SENSOR DATA #####################

#GET ALL SENSOR DATA
@app.route('/sensor', methods=['GET'])
def get_sensordata():
    sensors = Sensor_data.query.all()
    output = []
    for sens in sensors:
        sens_data = {}
        sens_data['hall_temperature'] = sens.hall_temperature
        sens_data['hall_motion'] = sens.hall_motion
        sens_data['kitchen_motion'] = sens.kitchen_motion
        sens_data['kitchen_firestatus'] = sens.kitchen_firestatus
        sens_data['external_brightness'] = sens.external_brightness
        sens_data['door_distance'] = sens.door_distance
        sens_data['date_read'] = sens.date_read
        sens_data['user_id'] = sens.user_id
        output.append(sens_data)

    return jsonify({'Sensor data' : output})


#ADD SENSOR DATA
@app.route ('/sensor', methods = ['POST'])
def add_sensorreading():
    data = request.get_json()
    new_reading = Sensor_data(hall_temperature = data['hall_temperature'], hall_motion = data['hall_motion'],kitchen_motion = data['kitchen_motion'], kitchen_firestatus = data['kitchen_firestatus'], external_brightness = data['external_brightness'], door_distance = data['door_distance'],date_read = datetime.now(), user_id = data['user_id'])

    db.session.add(new_reading)
    db.session.commit()
    return jsonify({'message': 'New sensor reading added!'})



################ ACTUATOR DATA #######################

#GET ALL ACTUATOR DATA
@app.route('/actuator', methods=['GET'])
def get_actuatordata():
    actuators = Actuator_data.query.all()
    output = []
    for act in actuators:
        act_data = {}
        act_data['hall_light'] = act.hall_light
        act_data['hall_fan'] = act.hall_fan
        act_data['kitchen_light'] = act.kitchen_light
        act_data['kitchen_blender'] = act.kitchen_blender
        act_data['kitchen_buzzer'] = act.kitchen_buzzer
        act_data['kitchen_stove'] = act.kitchen_stove
        act_data['external_light'] = act.external_light
        act_data['door_buzzer'] = act.door_buzzer
        act_data['user_id'] = act.user_id
        act_data['date_read'] = act.date_read
        output.append(act_data)

    return jsonify({'Actuator data' : output})


#ADD ACTUATOR DATA
@app.route ('/actuator', methods = ['POST'])
def add_actuatorreading():
    data = request.get_json()
    new_reading = Actuator_data(hall_fan = data['hall_fan'], hall_light = data['hall_light'], kitchen_light = data['kitchen_light'], kitchen_buzzer = data['kitchen_buzzer'], external_light = data['external_light'], door_buzzer = data['door_buzzer'], kitchen_blender = data['kitchen_blender'], kitchen_stove = data['kitchen_stove'], date_read = datetime.now(), user_id = data['user_id'], state = data['state'])

    db.session.add(new_reading)
    db.session.commit()
    return jsonify({'message': 'New actuator reading added!'})

#################################################################
# CONTROL MODE
class whichmode:
    mode = "automatic"

class whichcontrol:
    pinName = "null"
    pinMode = "nothing"

@app.route ('/controlmode/<modeType>')
def changeMode(modeType):
    global mode
    if modeType == "manual":
#        mode="manual"
        whichmode.mode = "manual"
    elif modeType == "automatic":
        whichmode.mode ="automatic"
    return jsonify({'mode': whichmode.mode})
        
@app.route ('/controls/<pin>/<state>')
def controls(pin,state):
    whichcontrol.pinName = pin
    whichcontrol.pinMode = state
    return jsonify({whichcontrol.pinName:whichcontrol.pinMode})
    
@app.route ('/controlmode', methods=['GET'])
def get_mode():
#    global mode 
    return whichmode.mode

@app.route ('/controls', methods=['GET'])
def get_controls():
    ctrldata = {}
    ctrldata['pinName'] = whichcontrol.pinName
    ctrldata['pinMode']= whichcontrol.pinMode
    
    return ctrldata


####################################################################
# REPORTS

@app.route ('/report', methods =['POST'])
def add_report():
	data = request.get_json()
	new_report = Reports(report = data['report'],  user_id = data['user_id'], date_sent = datetime.now())
	db.session.add(new_report)
	db.session.commit()
	return jsonify({'message': 'New consumption log added'}) 



########################################################################


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
    

