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

from feature_functions import *
features  = [down, dwell, flight, down_down]
detectors = [checkTimings, checkTimingsK]

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        testTimings = []
        for compute_feature in features:
          testTimings.append(compute_feature(json.loads(request.form.get('timings'))))
        loginSuccess = False
        results = [[False for i in features] for j in detectors]
        if checkLogin(username, password):
            loginSuccess = True
            realTimings = getTimings(username,password)
            realTimingsData = []
            for f in features:
              realTimingsData.append(f(json.loads(realTimings)))

            cov_matrix = []
            meanTimings = []
            for timingData in realTimingsData:
              cov_matrix.append(computeCovarianceMatrix(timingData))
              meanTimings.append(getMedianTiming(timingData))

            thresholds = []
            for processedData in zip(realTimingsData, cov_matrix):
              thresholds.append(computeThreshold(processedData[0],processedData[1]))

            results[0] = [checkTimingsK(data[0], data[1], data[2], 3, data[3]) for data in zip(testTimings, realTimingsData, cov_matrix, thresholds)]
            results[1] = [checkTimings(data[0], data[1], data[2], data[3]) for data in zip(testTimings, meanTimings, cov_matrix, thresholds)]

        return render_template('login.html', output=testTimings, 
                loginSuccess=loginSuccess, timingSuccessMean=results[1], timingSuccessK=results[0])
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

if __name__ == '__main__':
    app.debug=True
    app.run()
