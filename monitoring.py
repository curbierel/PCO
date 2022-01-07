from re import L
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User,lesBD,notations
from . import db
import json
from flask_wtf import FlaskForm
from wtforms import SubmitField
from matplotlib.figure import Figure

monitoring = Blueprint('monitoring', __name__)



@monitoring.route('/monitoring', methods=['GET', 'POST'])
@login_required
def monitor():
    pass
    return render_template("monitoring.html",user=current_user)
