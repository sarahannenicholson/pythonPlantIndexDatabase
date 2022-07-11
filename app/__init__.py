from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# creating the flask application
app = Flask(__name__)
app.config.from_object(Config)

# variable for database
db = SQLAlchemy(app)

from app import views
