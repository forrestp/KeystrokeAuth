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
from features import *
features = [(dwell, 1), (down, 1), (flight, 1), (down_down, 1)]
detectors = [(checkTimings, 1), (checkTimingsK, 1)]

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        results = []
        username = request.form.get('username')
        password = request.form.get('password')
        testTimings = []
        for x in features:
            testTimings.append(x[0](json.loads(request.form.get('timings'))))
        loginSuccess = False
        for x in detectors:
            results.append([False]*len(features))
        if checkLogin(username, password):
            loginSuccess = True
            realTimings = getTimings(username,password)
            realTimingsData = [x[0](json.loads(realTimings)) for x in features]
            cov_matrix = [computeCovarianceMatrix(x) for x in realTimingsData]
            meanTimings = [getMedianTiming(x) for x in readTimingsData]
#            [y[0](*x, ) for x in zip(testTimings, realTimingsData, cov_matrix) for y in detectors]
            timingSuccessK[0] = checkTimingsK(testTimings[0], realTimingsData[0], cov_matrix[0], 3)
            timingSuccessK[1] = checkTimingsK(testTimings[1], realTimingsData[1], cov_matrix[1], 3, 41)
            timingSuccessK[2] = checkTimingsK(testTimings[2], realTimingsData[2], cov_matrix[2], 3, 9)
            timingSuccessK[3] = checkTimingsK(testTimings[3], realTimingsData[3], cov_matrix[3], 3, 24.5)
            timingSuccessMean[0] = checkTimings(testTimings[0], meanTimings[0], cov_matrix[0])
            timingSuccessMean[1] = checkTimings(testTimings[1], meanTimings[1], cov_matrix[1], 42.5)
            timingSuccessMean[2] = checkTimings(testTimings[2], meanTimings[2], cov_matrix[2], 9)
            timingSuccessMean[3] = checkTimings(testTimings[3], meanTimings[3], cov_matrix[3], 25.0)
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

if __name__ == '__main__':
    app.debug=True
    app.run()
