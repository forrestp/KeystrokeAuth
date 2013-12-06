#!/usr/bin/python

from flask import Flask, render_template, request, json
from flask.ext.sqlalchemy import SQLAlchemy
from models import *
from rhythmCheck import *

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        testTimings = json.loads(request.form.get('timings'))
        loginSuccess = False
        timingSuccess = False
        if checkLogin(username, password):
            loginSuccess = True
            realTimings = User.query.filter_by(username=username).first().timings
            timingSuccess = checkTimings(parseTimings(testTimings), realTimings)
        return render_template('login.html', output=testTimings, 
                loginSuccess=loginSuccess, timingSuccess=timingSuccess)
    else:
        return render_template('login.html')
 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        timings = json.loads(request.form.get('timings'))
        success = registerUser(username, password, parseTimings(timings))
        return render_template('register.html', success=success)
    else:
        return render_template('register.html')
       
def checkLogin(username, password):
    user = User.query.filter_by(username=username).first() 
    if user is None:
        return False
    return user.password == password

def registerUser(username, password, timings):
    if User.query.filter_by(username=username).first() is not None:
        return False
    x = User(username, password, timings)
    db.session.add(x)
    db.session.commit()
    return True

''' Just work with down timings for now '''
def parseTimings(timings):
    return [t['down'] for t in timings]

if __name__ == '__main__':
    app.debug=True
    app.run()
