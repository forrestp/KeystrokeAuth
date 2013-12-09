from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(180))
    salt = db.Column(db.String(128))
    timings = db.Column(db.Text, unique=False)

    def __init__(self, username, password, salt,  timings):
        self.username = username
        self.password = password 
        self.salt = salt
        self.timings = timings 

    def __repr__(self):
        return '<User %r>' % self.username
