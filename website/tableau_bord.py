from re import L
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User,lesBD,notations
from . import db
import json
from flask_wtf import FlaskForm
from wtforms import SubmitField

tableau_bord = Blueprint('tableau_bord', __name__)
class critiqueBD(FlaskForm):
   submit = SubmitField("Sauver la critique")

@tableau_bord.route('/tableau_bord', methods=['GET', 'POST'])
@login_required
def tableau_borD():
    formCritiqueBD=critiqueBD()
    if request.method == 'POST':
        note = request.form.get('note')
        if request.form['lanote']:
            if len(note) < 8:
                from sqlalchemy import select
                stmt = select(User.first_name)
                new_note = Note(data=note, user_id=current_user.id,titre=request.form['titre'],auteur=stmt, note=request.form['lanote'])
                db.session.add(new_note)
                db.session.commit()
                flash('Note ajoutée sans critique ou avec une petite critique.', category='error')
            else:
                from sqlalchemy import select
                stmt = select(User.first_name)
                new_note = Note(data=note, user_id=current_user.id,titre=request.form['titre'],auteur=stmt, note=request.form['lanote'])
                db.session.add(new_note)
                db.session.commit()
                flash('Note added!', category='success')
        else:
            flash('Erreur la BD n\'est pas notée', category='error')
    
    s=lesBD.query.with_entities(lesBD.titreC)
    n=notations.query.with_entities(notations.note)
    return render_template("tableau_bord.html", user=current_user,lstTitre=s,lstnote=n,formBD=formCritiqueBD)


@tableau_bord.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
