from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from app import app, db
from app.dbmodels import PlantDatabase
from sqlalchemy.sql import text
from app.form import ContactForm, SearchForm
from dbconfig import DBConfig
from random import randint
import pandas as pd

app.config['SECRET_KEY'] = 'this is a secret key'

# creating and adding the mail config settings for sending messages via the contact us page
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'plantindexdatabase@gmail.com'
app.config["MAIL_PORT"] = ';q+zuJ&om'
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True

mail = Mail(app)


# setting the route for the pages
# index page
@app.route('/')
def index():
    with DBConfig.engine.begin() as conn:
        plantnames = conn.execute("SELECT * FROM plant_information WHERE plant_id = %s", randint(0, 27))
    return render_template('index.html', plantnames=plantnames, title='Home Page')


# about page
@app.route('/about')
def about():
    return render_template('about.html', title='About Us')


# contact us page
@app.route('/contact', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('contact.html', title='Contact Us', form=form)
        else:
            name = request.form["name"]
            email = request.form["email"]
            subject = request.form["subject"]
            message = request.form["message"]
            res = pd.DataFrame({'name': name, 'email': email, 'subject': subject, 'message': message}, index=[0])
            res.to_csv('./contactusMessage.csv')
            flash('Message Sent!')
            return redirect(url_for('contact'))
    elif request.method == 'GET':
        return render_template('contact.html', title='Contact Us', form=form)


# privacy policy page
@app.route('/privacy')
def privacy():
    return render_template('privacy.html', title='Privacy Policy')


# pass to navbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


# search function for the nav bar
@app.route('/searchbar', methods='POST')
def searchbar():
    form = SearchForm()
    plants = PlantDatabase.query
    if form.validate_on_submit():
        plants.searched = form.searched.data


# links page
@app.route('/links')
def links():
    return render_template('links.html', title='Affiliate Links')


# filterable catalog page
# takes data from the selected table ('use ...') and parses
# with the .execute command to display as list on the page
@app.route('/catalog')
def catalog():
    with DBConfig.engine.begin() as conn:
        plantnames = conn.execute("SELECT * FROM plant_information")
    return render_template('catalog.html', plantnames=plantnames, title='Plant Catalog')


# search page
@app.route('/search')
def search():
    return render_template('search.html', title='Plant Search')


# map page
@app.route('/map')
def map():
    return render_template('map.html', title='Map')


# calendar page
@app.route('/calendar')
def calendar():
    return render_template('calendar.html', title='Planting Calendar')


# plant info page
# to link to individual plant item pages
# currently works when entering the url manually
# does not work by clicking the link in the catalog page
@app.route('/plantinfo/<plant_names>')
def plantinfo(plant_names):
    with DBConfig.engine.begin() as conn:
        plantnames = conn.execute("SELECT * FROM plant_information")
    return render_template('plantinfo.html', plantnames=plantnames, plant_names=plant_names)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404 Error')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', title='Internal Server Error')
