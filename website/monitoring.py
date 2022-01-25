from re import L
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User, bedetheque,lesBD,notations,recommandations
from . import db
import json
from flask_wtf import FlaskForm
from wtforms import SubmitField
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import pandas as pd
monitoring = Blueprint('monitoring', __name__)

class MonitorBD(FlaskForm):
   submit = SubmitField("Supprimer cet utilisateur")


@monitoring.route('/monitoring', methods=['GET', 'POST'])
@login_required
def monitor():
    MBD=MonitorBD()
    Ut=User.query.with_entities(User.id,User.first_name).all()
    return render_template("monitoring.html",user=current_user,dfAlch=Ut,MBD=MBD)



@monitoring.route('/delete-user', methods=['POST'])
def delete_user():    
    user = json.loads(request.data)
    print(user)
    userFN=user['first_name']
    userbyID = User.query.filter_by(first_name=userFN).first()
    userID=userbyID.id
    reco = bedetheque.query.filter_by(user_id=userID).all()
    print(reco)
    suser = User.query.get(userID)
    db.session.delete(suser)
    db.session.commit()
    db.session.close()
    return jsonify({})