from flask import render_template
from app import app, db
from app.dbmodels import PlantDatabase
from sqlalchemy.sql import text


# setting the route for the pages
# index page
@app.route('/')
def index():
    return render_template('index.html')


# about page
@app.route('/about')
def about():
    return render_template('about.html')


# contact us page
@app.route('/contact')
def contact():
    return render_template('contact.html')


# privacy policy page
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


# links page
@app.route('/links')
def links():
    return render_template('links.html')


# filterable catalog page
# takes data from the selected table ('use ...') and parses
# with the .execute command to display as list on the page
@app.route('/catalog')
def catalog():
    plantnames = PlantDatabase.query.order_by(PlantDatabase.plant_name).all()
    return render_template('catalog.html', plantnames=plantnames)


# search page
@app.route('/search')
def search():
    return render_template('search.html')


# map page
@app.route('/map')
def map():
    return render_template('map.html')


# calendar page
@app.route('/calendar')
def calendar():
    return render_template('calendar.html')


# plant info page
# to link to individual plant item pages
# currently works when entering the url manually
# does not work by clicking the link in the catalog page
@app.route('/plantinfo/<plant_names>')
def plantinfo(plant_names):
    plantnames = PlantDatabase.query.filter_by(plant_name=plant_names).order_by(PlantDatabase.plant_name).all()
    return render_template('plantinfo.html', plantnames=plantnames, plant_names=plant_names)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')


# testing the database connection
@app.route('/testing1')
def testdb():
    try:
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
