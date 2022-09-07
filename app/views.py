from flask import render_template, request, flash, redirect, url_for
from app import app
from app.form import ContactForm
from dbconfig import DBConfig
from random import randint
import pandas as pd
from flask_cors import CORS

# bogus secret key
# needed for the search function via nav bar to work
# set up better security at a later date
app.config['SECRET_KEY'] = 'this is a secret key'


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


# setting the route for the pages
# index page
@app.route('/')
def index():
    with DBConfig.engine.begin() as conn:
        randnum = randint(0, 27)
        # currently takes a randint between 0-27 (current entries in the db) and displays on the home page
        # to show the "plant of the day" etc item
        # to work out at a later date how to specify a specific plant per actual week
        # and how to take the number of entries from the database and use that here instead of hard coding
        plantnames = conn.execute("SELECT * FROM plant_information WHERE plant_id = '{0}'".format(randnum))
    return render_template('index.html', plantnames=plantnames, title='Home Page')


# about page for the "company"
@app.route('/about')
def about():
    return render_template('about.html', title='About Us')


# contact us page
@app.route('/contact', methods=["GET", "POST"])
def contact():
    # uses a flask form and takes the users feedback and saves to a .csv file currently
    # need to work out if it can be used via email or something else so as we don't need to dw the file from
    # the aws servers each time
    # currently only saves 1 entry to the file and overrides every time a new form is processed
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
            res.to_csv('./contactusMessage.csv') # name of the saved .csv file that stores the messages
            flash('Message Sent!')
            return redirect(url_for('contact'))
    elif request.method == 'GET':
        return render_template('contact.html', title='Contact Us', form=form)


# privacy policy page
@app.route('/privacy')
def privacy():
    return render_template('privacy.html', title='Privacy Policy')


# links page
@app.route('/links')
def links():
    return render_template('links.html', title='Affiliate Links')


# catalog page
# currently displays all entries in the database with no filters
# later needs to implement a shortcut with the alphabet in order to quickly jump between entries
@app.route('/catalog')
def catalog():
    with DBConfig.engine.begin() as conn:
        plantnames = conn.execute("SELECT * FROM plant_information")
    return render_template('catalog.html', plantnames=plantnames, title='Plant Catalog')


# search page
# searches through the database and pulls plants based on the following filters
# season, type, cycle and zone
# other filters can be implemented later based on what could be required
@app.route('/search', methods=['GET', 'POST'])
def search():
    with DBConfig.engine.begin() as conn:
        plantnames = conn.execute("SELECT * FROM plant_information")
    if request.method == 'POST':
        seasonValue = '%%' + request.form.get("seasonValue") + '%%'
        typeValue = request.form.get("typeValue")
        cycleValue = request.form.get("cycleValue")
        zoneValue = '%%' + request.form.get("zoneValue") + '%%'  # escape the SQL values
        print(seasonValue, typeValue, cycleValue, zoneValue)
        with DBConfig.engine.begin() as conn:
            plantnames = conn.execute("SELECT * from plant_information WHERE pref_season LIKE '{0}' "
                                      "AND plant_type LIKE '{1}' "
                                      "AND life_cycle LIKE '{2}' "
                                      "AND hardiness_zone LIKE '{3}'".format(seasonValue, typeValue, cycleValue, zoneValue))
        if plantnames.rowcount == 0:
            print("In the testing loop")
    return render_template('search.html', title='Plant Search', plantnames=plantnames)


# map page
@app.route('/map')
def plantmap():
    return render_template('map.html', title='Map')


# calendar page
@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    labels = []
    values = []
    data = []
    plantnames = None
    if request.method == 'POST':
        seasonValue = '%%' + request.form.get("seasonValue") + '%%'
        typeValue = request.form.get("typeValue")
        if typeValue == "*":
            with DBConfig.engine.begin() as conn:
                plantnames = conn.execute("SELECT plant_name, plant_id, plant_type FROM plant_information "
                                          "WHERE pref_season LIKE '{0}'".format(seasonValue))
                for item in plantnames:
                    print(item)
                    labels.append('"' + item[0] + '",')
                    values.append(item[1])
                    print(labels)
                    print(values)
        with DBConfig.engine.begin() as conn:
            plantnames = conn.execute("SELECT plant_name, plant_id FROM plant_information WHERE pref_season LIKE '{0}'"
                                      "AND plant_type LIKE '{1}'".format(seasonValue, typeValue))
            for item in plantnames:
                print(item)
                # data.append(['"' + item.plant_name + '",', item.plant_id])
                labels.append('"' + item[0] + '",')
                # TODO:
                # this needs to be formatted so that there is a comma seperating the list when taken across to the .js page
                # this will need to be done in javascript
                values.append(item[1])
                print(labels)
                print(values)
            # data.append([plantnames.plant_name, plantnames.plant_id])
            # print(data)
    return render_template('calendar.html', title='Planting Calendar', labels=labels, values=values)


# plant info page
# to link to individual plant item pages
# currently works when entering the url manually
# currently works by clicking the link in the catalog page
@app.route('/plantinfo/<plant_names>')
def plantinfo(plant_names):
    with DBConfig.engine.begin() as conn:
        plantnames = conn.execute("SELECT * FROM plant_information")
    return render_template('plantinfo.html', plantnames=plantnames, plant_names=plant_names)


# takes the entered string from the search box in the navbar and parses against all columns in the
# database to find matching items
@app.route('/searchbar', methods=['GET', 'POST'])
def searchbar():
    searched = '%%' + request.form.get("searchedPlant") + '%%'
    print(searched)
    error = None
    if request.method == 'POST':
        with DBConfig.engine.begin() as conn:
            plantnames = conn.execute("SELECT * FROM plant_information WHERE plant_name LIKE '{0}'  "
                                      "OR variety_names LIKE '{0}' OR alt_names LIKE '{0}'  OR family_name LIKE '{0}'"
                                      "OR plant_type LIKE '{0}'  OR pref_season LIKE '{0}' OR life_cycle LIKE '{0}' "
                                      "OR hardiness_zone LIKE '{0}' OR sun_exposure LIKE '{0}' OR water_needs LIKE '{0}'"
                                      "OR maint_nneds LIKE '{0}' OR soil_type LIKE '{0}' OR soil_ph LIKE '{0}' "
                                      "OR soil_drain LIKE '{0}' OR start_type LIKE '{0}' OR spacing_needs LIKE '{0}' "
                                      "OR gorw_time_seed LIKE '{0}' OR grow_time_sling LIKE '{0}' "
                                      "OR harvest_recommendations LIKE '{0}' OR pref_nutrients LIKE '{0}' "
                                      "OR companion_plants LIKE '{0}' OR avoid_with LIKE '{0}' OR crop_rotate LIKE '{0}'"
                                      "OR instructions LIKE '{0}' OR instructions LIKE '{0}' OR general_info LIKE '{0}'"
                                      "OR preservation_ideas LIKE '{0}'".format(searched))
    elif request.method == 'GET':
        flash("Please try again")
        return redirect('searchbar.html')
    else:
        flash('Search returned no results')
        redirect(url_for('searchbar'))
    return render_template('searchbar.html', plantnames=plantnames, error=error)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404 Error')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', title='Internal Server Error')


@app.route('/testing')
def testing():
    return render_template('testing.html')
