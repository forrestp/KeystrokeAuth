#!/usr/bin/python

from flask import Flask, render_template, request, json
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from models import *
from rhythmCheck import *
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2 
from Crypto import Random
import os, hashlib, random, base64

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)
admin=Admin(app)
admin.add_view(ModelView(User, db.session))
if not os.path.isfile("test.db"):
    with app.app_context():
        db.create_all()



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        testTimings = []
        testTimings.append(down(json.loads(request.form.get('timings'))))
        testTimings.append(dwell(json.loads(request.form.get('timings'))))
        testTimings.append(flight(json.loads(request.form.get('timings'))))
        testTimings.append(down_down(json.loads(request.form.get('timings'))))
        loginSuccess = False
        timingSuccessK    = [False, False, False, False]
        timingSuccessMean = [False, False, False, False]
        if checkLogin(username, password):
            loginSuccess = True
            realTimings = getTimings(username,password)
            realTimingsData = []
            realTimingsData.append(down(json.loads(realTimings)))
            realTimingsData.append(dwell(json.loads(realTimings)))
            realTimingsData.append(flight(json.loads(realTimings)))
            realTimingsData.append(down_down(json.loads(realTimings)))

            cov_matrix = []
            cov_matrix.append(computeCovarianceMatrix(realTimingsData[0]))
            cov_matrix.append(computeCovarianceMatrix(realTimingsData[1]))
            cov_matrix.append(computeCovarianceMatrix(realTimingsData[2]))
            cov_matrix.append(computeCovarianceMatrix(realTimingsData[3]))

            meanTimings = []
            meanTimings.append(getMedianTiming(realTimingsData[0]))
            meanTimings.append(getMedianTiming(realTimingsData[1]))
            meanTimings.append(getMedianTiming(realTimingsData[2]))
            meanTimings.append(getMedianTiming(realTimingsData[3]))

            thresholds = []
            thresholds.append(computeThreshold(realTimingsData[0]),cov_matrix[0])
            thresholds.append(computeThreshold(realTimingsData[1]),cov_matrix[1])
            thresholds.append(computeThreshold(realTimingsData[2]),cov_matrix[2])
            thresholds.append(computeThreshold(realTimingsData[3]),cov_matrix[3])
            print thresholds

            timingSuccessK[0] = checkTimingsK(testTimings[0], realTimingsData[0], cov_matrix[0], 3, thresholds[0])
            timingSuccessK[1] = checkTimingsK(testTimings[1], realTimingsData[1], cov_matrix[1], 3, thresholds[1])
            timingSuccessK[2] = checkTimingsK(testTimings[2], realTimingsData[2], cov_matrix[2], 3, thresholds[2])
            timingSuccessK[3] = checkTimingsK(testTimings[3], realTimingsData[3], cov_matrix[3], 3, thresholds[3])

            timingSuccessMean[0] = checkTimings(testTimings[0], meanTimings[0], cov_matrix[0], thresholds[0])
            timingSuccessMean[1] = checkTimings(testTimings[1], meanTimings[1], cov_matrix[1], thresholds[1])
            timingSuccessMean[2] = checkTimings(testTimings[2], meanTimings[2], cov_matrix[2], thresholds[2])
            timingSuccessMean[3] = checkTimings(testTimings[3], meanTimings[3], cov_matrix[3], thresholds[3])

        return render_template('login.html', output=testTimings, 
                loginSuccess=loginSuccess, timingSuccessMean=timingSuccessMean, timingSuccessK=timingSuccessK)
    else:
        return render_template('login.html')
 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print "register: request.method is POST"
        username = request.form.get('username')
        password = request.form.get('password')
        timings = request.form.get('timings')
        success = registerUser(username, password, timings)
        print "registered user"
        return render_template('register.html', success=success)
    else:
        return render_template('register.html')
       
def checkLogin(username, password):
    user = User.query.filter_by(username=username).first() 
    if user is None:
        return False
    salt = user.salt
    cryptPass = PBKDF2(password, salt, 32, 1000)
    return base64.b64decode(user.password) == cryptPass

def registerUser(username, password, timings):
    if User.query.filter_by(username=username).first():
        return False
    salt = base64.b64encode(Random.new().read(32))
    password_hash = PBKDF2(password, salt, 32, 1000)

    salt2 = base64.b64encode(Random.new().read(32))
    iv = Random.new().read(AES.block_size)
    aes_hash = PBKDF2(password, salt2, 32, 1000)
    aes = AES.new(aes_hash, AES.MODE_CFB, iv)
    encrypted_timings = base64.b64encode(iv + aes.encrypt(timings))

    u = User(username, base64.b64encode(password_hash), salt, salt2, encrypted_timings)
    db.session.add(u)
    db.session.commit()
    return True

def getTimings(username, password):
    if checkLogin(username, password):
        user = User.query.filter_by(username=username).first() 
        aes_hash = PBKDF2(password, user.salt2, 32, 1000)
        encrypted_timings = base64.b64decode(user.timings)
        iv = encrypted_timings[:16]
        aes = AES.new(aes_hash, AES.MODE_CFB, iv)
        return aes.decrypt(encrypted_timings[16:])
    return ""

''' The various four features/metrics we use for comparison.'''
def down(data):
  if (isinstance(data[0], list)):
    return map(down, data)
  else:
    return [d.get('down',0) for d in data]

def dwell(data):
  if (isinstance(data[0], list)):
    return map(dwell, data)
  else:
    return [d.get('up',0) - d.get('down',0) for d in data]

def flight(data):
  if (isinstance(data[0], list)):
    return map(flight, data)
  else:
    return [data[i+1].get('down',0) - data[i].get('up',0) for i in range(len(data)-1)]

def down_down(data):
  if (isinstance(data[0], list)):
    return map(down_down, data)
  else:
    return [data[i+1].get('down',0) - data[i].get('down',0) for i in range(len(data)-1)]


if __name__ == '__main__':
    app.debug=True
    app.run()
