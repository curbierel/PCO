from sqlite3.dbapi2 import TimestampFromTicks
from flask import Blueprint, url_for, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import update
from . import db
from .fonction import get_image, get_title, get_index
from .models import lesBD, mse2, recommandations
import json
from flask_wtf import FlaskForm
from wtforms import SubmitField
import pandas as pd
import sqlite3
import datetime
from sqlalchemy import desc
import re

class choiceBD(FlaskForm):
   submit = SubmitField("Voir nos propositions")

class choiceDate(FlaskForm):
   submit = SubmitField("Afficher les recommandations pour la période choisie")


faire_reco = Blueprint('faire_reco', __name__)
dfCo=pd.read_csv('mse2.csv',sep='\t')
connecteur=sqlite3.connect('database.db', check_same_thread=False)

dflstBD=pd.read_sql_query("SELECT titreC,image FROM lesBD",connecteur)# DataFrame listant les BD et leurs résuméimport spacy
dflstBD['titre']=dflstBD['titrec']

@faire_reco.route('/faire_reco', methods=['GET', 'POST'])
@login_required
def faire_recO():
   debut="2021-12-01"
   fin="2022-03-01"
   areco=None
   lstBD=t=['']
   pred=images=[]
   titre=[]
   titre_choisi=None
   formChioiceDate = choiceDate()
   formChioiceBD = choiceBD()
   if request.method == 'POST' :
         try:
            if formChioiceBD.submit.data:
               haricot=request.form['titre']
               areco=str(int(get_index(dflstBD,haricot)))    # C'est l'ID de la BD(qui va de 1 à ....)
         except :
            debut=request.form['debut']
            fin=request.form['fin']
         

   if areco:
      t=mse2.query.with_entities(mse2.reco_1,mse2.reco_2,mse2.reco_3,mse2.reco_4,mse2.reco_5).filter_by(id=areco)
      for t_tmp in t:
         for it,tt_tmp in enumerate(t_tmp):
               pred+=[get_title(dfCo,tt_tmp)]
               if recommandations.query.filter((recommandations.user_id==current_user.id)&(recommandations.titre==get_title(dfCo,tt_tmp))).all():
                  db.session.query(recommandations).filter(recommandations.user_id==current_user.id or recommandations.titre==get_title(dfCo,tt_tmp)).update({recommandations.nb:recommandations.nb+1})
                  db.session.commit()
               else:
                  IMG =lesBD.query.with_entities(lesBD.image).filter_by(titreC=get_title(dfCo,tt_tmp)).first()
                  new_reco = recommandations(titre=get_title(dfCo,tt_tmp), user_id=current_user.id,nb=1,image=remove_tags(IMG))
                  db.session.add(new_reco)
      titre_choisi=get_title(dfCo,int(areco))
      db.session.commit()

   
   t=lesBD.query.with_entities(lesBD.id,lesBD.titreC,lesBD.image)
   r=recommandations.query.with_entities(recommandations.titre,recommandations.id,recommandations.image).filter(recommandations.user_id == current_user.id).filter(recommandations.date<fin).filter(recommandations.date>debut).order_by(desc(recommandations.nb)).all()
   return render_template("faire_reco.html",user=current_user,lstBD=t, formBD=formChioiceBD,predict=pred,IMG=images,areco=areco,titre=titre_choisi,listeR=r,formDate=formChioiceDate,debut=debut,fin=fin)


@faire_reco.route('/delete-reco', methods=['POST'])
def delete_recO():
    reco = json.loads(request.data)
    recoid = reco['id']
    reco = recommandations.query.get(recoid)
    if reco:
        if reco.user_id == current_user.id:
            db.session.delete(reco)
            db.session.commit()

    return jsonify({})

def remove_tags(text) :
  TEXT=""
  text=str(text)
  for i in range  (2,len(text)-3):
    TEXT+=text[i]
  TEXT=re.sub('/couv', 'https://www.babelio.com/couv',TEXT)
  return TEXT

