from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import pymysql

# instance identifer - plant-index-database
# username - admin
# pw - admin123
# port - 3306
# hostname - plant-index-database.cyaimo2g0lsu.us-east-2.rds.amazonaws.com

# creating the flask application
application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:" \
                                                "admin123@plant-index-database.cyaimo2g0lsu." \
                                                "us-east-2.rds.amazonaws.com:" \
                                                "3306/plant_database"

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# connecting to the database located at aws servers
# db = pymysql.connect(host='plant-index-database.cyaimo2g0lsu.us-east-2.rds.amazonaws.com', user='admin',
# password='admin123')

# variable for database
db = SQLAlchemy(application)


# cursor for connection
# cursor = db.cursor()

# database table class for plant_information
class PlantDatabase(db.Model):
    __tablename__ = 'plant_information'
    plant_id = db.Column(db.Integer, primary_key=True)
    plant_name = db.Column(db.String)
    variety_names = db.Column(db.String)
    alt_names = db.Column(db.String)
    family_name = db.Column(db.String)
    plant_type = db.Column(db.String)
    pref_season = db.Column(db.String)
    life_cycle = db.Column(db.String)  # db.Enum('Perennial', 'Annual', 'Biennial', 'N//A'))
    hardiness_zone = db.Column(db.String)
    sun_exposure = db.Column(db.String)
    water_needs = db.Column(db.String)
    maint_nneds = db.Column(db.String)
    soil_type = db.Column(db.String)
    soil_ph = db.Column(db.String)
    soil_drain = db.Column(db.String)
    start_type = db.Column(db.String)
    spacing_needs = db.Column(db.String)
    gorw_time_seed = db.Column(db.String)
    grow_time_sling = db.Column(db.String)
    harvest_recommendations = db.Column(db.String)
    pref_nutrients = db.Column(db.String)
    companion_plants = db.Column(db.String)
    avoid_with = db.Column(db.String)
    crop_rotate = db.Column(db.String)
    instructions = db.Column(db.String)
    uses = db.Column(db.String)
    general_info = db.Column(db.String)
    preservation_ideas = db.Column(db.String)


# testing the database connection
@application.route('/testing1')
def testdb():
    try:
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text


# setting the route for the pages
# index page
@application.route('/')
def index():
    return render_template('index.html')


# about page
@application.route('/about')
def about():
    return render_template('about.html')


# contact us page
@application.route('/contact')
def contact():
    return render_template('contact.html')


# privacy policy page
@application.route('/privacy')
def privacy():
    return render_template('privacy.html')


# links page
@application.route('/links')
def links():
    return render_template('links.html')


# filterable catalog page
# takes data from the selected table ('use ...') and parses
# with the .execute command to display as list on the page
@application.route('/catalog')
def catalog():
    plantnames = PlantDatabase.query.order_by(PlantDatabase.plant_name).all()
    return render_template('catalog.html', plantnames=plantnames)


# search page
@application.route('/search')
def search():
    return render_template('search.html')


# map page
@application.route('/map')
def map():
    return render_template('map.html')


# calendar page
@application.route('/calendar')
def calendar():
    return render_template('calendar.html')


# plant info page
# to link to individual plant item pages
# currently works when entering the url manually
# does not work by clicking the link in the catalog page
@application.route('/plantinfo/<plant_names>')
def plantinfo(plant_names):
    plantnames = PlantDatabase.query.filter_by(plant_name=plant_names).order_by(PlantDatabase.plant_name).all()
    return render_template('plantinfo.html', plantnames=plantnames, plant_names=plant_names)


@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@application.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')


# to run the application
if __name__ == "__main__":
    application.run(debug=True)
