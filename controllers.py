from flask import Blueprint, render_template, request, url_for, redirect
from database_tables import PlantDatabase
from application import db

cursor = db.cursor()

auth_controllers = Blueprint('auth', __name__)
