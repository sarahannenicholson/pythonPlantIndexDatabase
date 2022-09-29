from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dbconfig import DBConfig
from flaskext.mysql import MySQL


# creating the flask application
application = Flask(__name__)
application.config.from_object(DBConfig)

# variable for database
db = SQLAlchemy(application)

mysql = MySQL()
mysql.init_app(application)

from app import views

