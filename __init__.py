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
        testTimings = parseTimings(json.loads(request.form.get('timings')))
        loginSuccess = False
        timingSuccessMean = False
        if checkLogin(username, password):
            loginSuccess = True
            realTimings = User.query.filter_by(username=username).first().timings
            realTimings = parseTimings2D(json.loads(realTimings))
            cov_matrix = computeCovarianceMatrix(realTimings)
            meanTimings = getMedianTiming(realTimings)
            # print meanTimings
            # print testTimings
            timingSuccessK = checkTimingsK(testTimings, realTimings, cov_matrix, 3)
            timingSuccessMean = checkTimings(testTimings, meanTimings, cov_matrix)
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

''' Just work with down timings for now '''
def parseTimings(timings):
    return [t['down'] for t in timings]

def parseTimings2D(timings):
    out = []
    for row in timings:
        temp = []
        for stroke in row:
            temp.append(stroke['down'])

        out.append(temp)
    return out

if __name__ == '__main__':
    app.debug=True
    app.run()
