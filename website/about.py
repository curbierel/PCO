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


about = Blueprint('about', __name__)

@about.route('/about', methods=['GET'])
@login_required
def ABOUT():
    
    return render_template("about.html", user=current_user)

