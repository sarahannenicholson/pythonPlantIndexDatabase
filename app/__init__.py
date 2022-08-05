from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dbconfig import DBConfig
from flask_mail import Mail


# creating the mail connection to send messages via the contact us page
mail = Mail()

# creating the flask application
app = Flask(__name__)
app.config.from_object(DBConfig)

# variable for database
db = SQLAlchemy(app)

from app import views

