from datetime import datetime
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from flask.ext.sqlalchemy import SQLAlchemy
from flask import session
db = SQLAlchemy()

#models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String())

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<email %r>" % self.email

class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    started = db.Column(db.DateTime)
    completed = db.Column(db.DateTime)
    hitId = db.Column(db.String(40))
    assignmentId = db.Column(db.String(40))
    img_0 = db.Column(db.Integer)
    img_1 = db.Column(db.Integer)
    img_2 = db.Column(db.Integer)
    img_3 = db.Column(db.Integer)
    img_4 = db.Column(db.Integer)
    img_5 = db.Column(db.Integer)
    img_6 = db.Column(db.Integer)
    img_7 = db.Column(db.Integer)
    img_8 = db.Column(db.Integer)
    img_9 = db.Column(db.Integer)
    img_10 = db.Column(db.Integer)
    img_11 = db.Column(db.Integer)

    def __init__(self, hitId, assignmentId):
        self.hitId = hitId
        self.assignmentId = assignmentId

    def complete(self):
        self.completed = datetime.now()

    def start(self):
        self.started = datetime.now()

    def string_format(self):
        s_format = "%d\t%s\t%s\t%s\t%s\t" % (self.id, self.started, self.completed, self.hitId, self.assignmentId)
        for i in range(0,12):
            s_format += str((getattr(self, "img_%d" % i))) + "\t"
        return s_format + "\n"
