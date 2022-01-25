from os import listdir
from re import L
import re
from traceback import print_tb
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from wtforms.fields import form

from .models import historique, lesBD,bedetheque, recommandations
from . import db
import sqlite3
import json
from flask_wtf import FlaskForm
from wtforms import SubmitField
import pandas as pd

from .recotitre import TsMesLivresNLP

home = Blueprint('home', __name__)
class ajouterBD(FlaskForm):
   submit = SubmitField("Je possède cette BD")

class MettreAjourHistorique(FlaskForm):
    submit = SubmitField("Mettre à jour")

@home.route('/', methods=['GET','POST'])
@login_required
def hoMe():
  HistoForm=MettreAjourHistorique()
  formBDtheque=ajouterBD()
  s=ListeBD=MesBD=[]
  titre=""
  
  if current_user.first_name != 'admin':
    titre=[]
    
    ListeBD=lesBD.query.with_entities(lesBD.titreC)
    MesBD=bedetheque.query.with_entities(bedetheque.image,bedetheque.id).filter_by(user_id=current_user.id)


    if request.method == 'POST':
      if formBDtheque.submit.data:
        if bedetheque.query.filter((bedetheque.user_id==current_user.id)&(bedetheque.titre==request.form['titre'])).all():
          flash('Vous possédez déja cette BD !!', category='error')
        else :      
          IMG =lesBD.query.with_entities(lesBD.image).filter_by(titreC=request.form['titre']).first()
          new_bd= bedetheque(titre=request.form['titre'], image=remove_tags(IMG),user_id=current_user.id)
          db.session.add(new_bd)
          db.session.commit()
          flash('Bedetheque MAJ', category='succcess')
          #print(TsMesLivresNLP('database.db',bedetheque))
        return render_template("home.html", user=current_user,ListeBD=ListeBD,MesBD=MesBD,titre=titre,formBD=formBDtheque)
      
  elif HistoForm.submit:
      print('YOTP')
      connecteur=sqlite3.connect('database.db')
      BD=pd.read_sql_query("SELECT id,titreC FROM lesBD",connecteur)
      RECO=pd.read_sql_query("SELECT * FROM recommandations",connecteur)
      utilisateurs=pd.read_sql_query("SELECT id FROM user",connecteur)    
      critiques=pd.read_sql_query("SELECT id FROM note",connecteur)
      connecteur.close()
      nbReco=RECO['nb'].sum()
      nbUtil=utilisateurs["id"].count()
      nbCri=critiques['id'].count()
      nbBD=BD['id'].count()
      from sqlalchemy import select
      new_historique = historique(nb_reco=int(nbReco),nb_user=int(nbUtil),nb_cri=int(nbCri),nb_bd=int(nbBD))
      db.session.add(new_historique)
      db.session.commit()
      db.session.flush()
      s=historique.query.with_entities(historique.nb_bd,historique.nb_cri,historique.nb_reco,historique.nb_user)
      return render_template("home.html",parametres=s,user=current_user,HistoForM=HistoForm)
  return render_template("home.html", user=current_user,ListeBD=ListeBD,MesBD=MesBD,titre=titre,formBD=formBDtheque,parametres=s,HistoForM=HistoForm)
    
    


   

def remove_tags(text) :
  TEXT=""
  text=str(text)
  for i in range  (2,len(text)-3):
    TEXT+=text[i]
  TEXT=re.sub('/couv', 'https://www.babelio.com/couv',TEXT)
  return TEXT


@home.route('/delete-BD', methods=['POST'])
def delete_bd():
    BD = json.loads(request.data)
    Id = BD['id']

    bd = bedetheque.query.get(Id)
    if bd:
        if bd.user_id == current_user.id:
            db.session.delete(bd)
            db.session.commit()

    return jsonify({})
