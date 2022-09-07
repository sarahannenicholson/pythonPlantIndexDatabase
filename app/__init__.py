from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dbconfig import DBConfig
from flaskext.mysql import MySQL


# creating the flask application
app = Flask(__name__)
app.config.from_object(DBConfig)

# variable for database
db = SQLAlchemy(app)

mysql = MySQL()
mysql.init_app(app)

from app import views

