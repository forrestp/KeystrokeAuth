#!/usr/bin/python

from flask import Flask, render_template, request, json
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from models import *
from rhythmCheck import *
import os, hashlib, pbkdf2, random, base64

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
        #testTimings.append(dwell(json.loads(request.form.get('timings'))))
        #testTimings.append(flight(json.loads(request.form.get('timings'))))
        #testTimings.append(down_down(json.loads(request.form.get('timings'))))
        loginSuccess = False
        timingSuccessK    = [False, False, False, False]
        timingSuccessMean = [False, False, False, False]
        if checkLogin(username, password):
            loginSuccess = True
            realTimings = User.query.filter_by(username=username).first().timings
            realTimingsData = []
            realTimingsData.append(down(json.loads(realTimings)))
            #realTimingsData.append(dwell(json.loads(realTimings)))
            #realTimingsData.append(flight(json.loads(realTimings)))
            #realTimingsData.append(down_down(json.loads(realTimings)))
            cov_matrix = []
            cov_matrix.append(computeCovarianceMatrix(realTimingsData[0]))
            #cov_matrix.append(computeCovarianceMatrix(realTimingsData[1]))
            #cov_matrix.append(computeCovarianceMatrix(realTimingsData[2]))
            #cov_matrix.append(computeCovarianceMatrix(realTimingsData[3]))
            meanTimings = []
            meanTimings.append(getMedianTiming(realTimingsData[0]))
            #meanTimings.append(getMedianTiming(realTimingsData[1]))
            #meanTimings.append(getMedianTiming(realTimingsData[2]))
            #meanTimings.append(getMedianTiming(realTimingsData[3]))
            # print meanTimings
            # print testTimings
            timingSuccessK[0] = checkTimingsK(testTimings[0], realTimingsData[0], cov_matrix[0], 3)
            #timingSuccessK[1] = checkTimingsK(testTimings[1], realTimingsData[1], cov_matrix[1], 3, 41)
            #timingSuccessK[2] = checkTimingsK(testTimings[2], realTimingsData[2], cov_matrix[2], 3, 9)
            #timingSuccessK[3] = checkTimingsK(testTimings[3], realTimingsData[3], cov_matrix[3], 3, 24.5)
            timingSuccessMean[0] = checkTimings(testTimings[0], meanTimings[0], cov_matrix[0])
            #timingSuccessMean[1] = checkTimings(testTimings[1], meanTimings[1], cov_matrix[1], 42.5)
            #timingSuccessMean[2] = checkTimings(testTimings[2], meanTimings[2], cov_matrix[2], 9)
            #timingSuccessMean[3] = checkTimings(testTimings[3], meanTimings[3], cov_matrix[3], 25.0)
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
    cryptPass = unicode(pbkdf2.PBKDF2(password, salt).hexread(32))  
    return user.password == cryptPass

def registerUser(username, password, timings):
    if User.query.filter_by(username=username).first():
        return False
    username = username
    salt = base64.urlsafe_b64encode(os.urandom(128))
    password = unicode(pbkdf2.PBKDF2(password, salt).hexread(32)) 
    timings = timings
    u = User(username, password, salt, timings)
    db.session.add(u)
    db.session.commit()
    return True

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
