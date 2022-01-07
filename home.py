from os import listdir
from re import L
import re
from flask import Blueprint, render_template, request, flash, jsonify
from flask.scaffold import _matching_loader_thinks_module_is_package
from flask_login import login_required, current_user
from wtforms.fields import form

from .models import lesBD,bedetheque, recommandations
from . import db
import sqlite3
import json
from flask_wtf import FlaskForm
from wtforms import SubmitField


home = Blueprint('home', __name__)
class ajouterBD(FlaskForm):
   submit = SubmitField("Je possède cette BD")

@home.route('/', methods=['GET','POST'])
@login_required
def hoMe():
    titre=[]
    formBDtheque=ajouterBD()
    ListeBD=lesBD.query.with_entities(lesBD.titreC)
    MesBD=bedetheque.query.with_entities(bedetheque.image).filter_by(user_id=current_user.id)


    if request.method == 'POST':
      if bedetheque.query.filter((bedetheque.user_id==current_user.id)&(bedetheque.titre==request.form['titre'])).all():
        flash('Vous possédez déja cette BD !!', category='error')
      else :      
        IMG =lesBD.query.with_entities(lesBD.image).filter_by(titreC=request.form['titre']).first()
        new_bd= bedetheque(titre=request.form['titre'], image=remove_tags(IMG),user_id=current_user.id)
        db.session.add(new_bd)
        db.session.commit()
        flash('Bedetheque MAJ', category='succcess')
  
  
    return render_template("home.html", user=current_user,ListeBD=ListeBD,MesBD=MesBD,titre=titre,formBD=formBDtheque)

def remove_tags(text) :
  TEXT=""
  text=str(text)

  print(54*'x',len(text),text[10])
  for i in range  (2,len(text)-3):
    TEXT+=text[i]
  TEXT=re.sub('/couv', 'https://www.babelio.com/couv',TEXT)
  return TEXT