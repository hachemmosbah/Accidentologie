from flask_login import UserMixin
from datetime import datetime
from . import db
from sqlalchemy import UniqueConstraint

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    date_created = db.Column(db.DateTime, default= datetime.utcnow)

    formdatas = db.relationship("Formdata", backref='user', cascade = 'all, delete-orphan', lazy = 'dynamic')
    formpreds = db.relationship("Formpred", backref='user', cascade = 'all, delete-orphan', lazy = 'dynamic')
    preds = db.relationship("Pred", backref='user', cascade = 'all, delete-orphan', lazy = 'dynamic')
    
    def __init__(self,name,email, password,date_created):
        self.name = name
        self.email = email
        self.password = password
        self.date_created = date_created

    def toString(self):
	    return ({'name':self.name, 'email':self.email})
    
class Formdata(db.Model):
    __tablename__ = 'formdata'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    year = db.Column(db.Integer)
    age1 = db.Column(db.Integer)
    age2 = db.Column(db.Integer)
    departement = db.Column(db.String(100))
    unhurt=db.Column(db.String(100))
    dead=db.Column(db.String(100))
    hospitalize=db.Column(db.String(100))
    hurt_light=db.Column(db.String(100))
    men=db.Column(db.String(100))
    women=db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __init__(self,year,age1,age2,departement,unhurt,dead,hospitalize,hurt_light,men,women,user_id):
       self.year = year
       self.age1 = age1
       self.age2 = age2
       self.departement = departement
       self.unhurt = unhurt
       self.dead = dead
       self.hospitalize = hospitalize
       self.hurt_light = hurt_light
       self.men = men
       self.women = women
       self.user_id = user_id

    def toString(self):
	    return ({'departement':self.departement, 'unhurt':self.unhurt
                ,'dead':self.dead, 'hospitalize':self.hospitalize, 'hurt_light':self.hurt_light
                , 'men':self.men, 'women':self.women})
    
class Formpred(db.Model):
    __tablename__ = 'formpred'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    year = db.Column(db.Integer)
    departement = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    location = db.Column(db.Integer)
    intersection = db.Column(db.Integer)
    light = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    pred = db.relationship("Pred", backref='formpred', cascade = 'all, delete-orphan', lazy = 'dynamic')

class Pred(db.Model):
    __tablename__ = 'pred'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    pred = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    formpred_id = db.Column(db.Integer, db.ForeignKey('formpred.id'), nullable = False)
