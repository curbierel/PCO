from . import DB_NAME, db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    titre=db.Column(db.String(100))
    auteur=db.Column(db.String(20))
    note= db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')


class lesBD(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serie=db.Column(db.String(150))
    titre = db.Column(db.String(150))
    titreC=db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    ean = db.Column(db.Integer, unique=True)
    genres= db.Column(db.String(150))
    resume= db.Column(db.String(9999))
    auteur=db.Column(db.String(50))
    image=db.Column(db.String(100))
    dessinateur=db.Column(db.String(50))
    rating= db.Column(db.Integer)



class mse2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reco_1 = db.Column(db.Integer)
    reco_2 = db.Column(db.Integer)
    reco_3 = db.Column(db.Integer)
    reco_4 = db.Column(db.Integer)
    reco_5 = db.Column(db.Integer)
    titre = db.Column(db.String(150))

class notations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note=db.Column(db.Integer)

class recommandations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre=db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    nb = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    image=db.Column(db.String(100), db.ForeignKey('lesBD.image'))


class bedetheque(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre=db.Column(db.String(100), db.ForeignKey('lesBD.titreC'))
    image=db.Column(db.String(100), db.ForeignKey('lesBD.image'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class historique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nb_user = db.Column(db.Integer)
    nb_cri = db.Column(db.Integer)
    nb_reco = db.Column(db.Integer)
    nb_bd = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())


