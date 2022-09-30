from flask import render_template, request, flash, redirect, url_for
from app import application
from app.form import ContactForm
from dbconfig import DBConfig
from random import randint
import pandas as pd

# bogus secret key
# needed for the search function via nav bar to work
# set up better security at a later date
application.config['SECRET_KEY'] = 'this is a secret key'


@application.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


# setting the route for the pages
# index page
@application.route('/')
def index():
    with DBConfig.engine.begin() as conn:
        randnum = randint(0, 31)
        # currently takes a randint between 0-27 (current entries in the db) and displays on the home page
        # to show the "plant of the day" etc item
        # to work out at a later date how to specify a specific plant per actual week
        # and how to take the number of entries from the database and use that here instead of hard coding
        plantnames = conn.execute("SELECT * FROM plant_information WHERE plant_id = '{0}'".format(randnum))
    return render_template('index.html', plantnames=plantnames, title='Home Page')


# about page for the "company"
@application.route('/about')
def about():
    return render_template('about.html', title='About Us')


# contact us page
@application.route('/contact', methods=["GET", "POST"])
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
            res.to_csv('./contactusMessage.csv')  # name of the saved .csv file that stores the messages
            flash('Message Sent!')
            return redirect(url_for('contact'))
    elif request.method == 'GET':
        return render_template('contact.html', title='Contact Us', form=form)


# privacy policy page
@application.route('/privacy')
def privacy():
    return render_template('privacy.html', title='Privacy Policy')


# links page
@application.route('/links')
def links():
    return render_template('links.html', title='Affiliate Links')


# catalog page
# currently displays all entries in the database with no filters
# later needs to implement a shortcut with the alphabet in order to quickly jump between entries
@application.route('/catalog')
def catalog():
    with DBConfig.engine.begin() as conn:
        plantnames = conn.execute("SELECT * FROM plant_information")
    return render_template('catalog.html', plantnames=plantnames, title='Plant Catalog')


# search page
# searches through the database and pulls plants based on the following filters
# season, type, cycle and zone
# other filters can be implemented later based on what could be required
@application.route('/search', methods=['GET', 'POST'])
def search():
    with DBConfig.engine.begin() as conn:
        # initial load of all items in database into search page
        plantnames = conn.execute("SELECT * FROM plant_information")

    if request.method == 'POST':
        # runs search when the searched button pressed
        seasonValue = request.form.get("seasonValue")
        typeValue = request.form.get("typeValue")
        cycleValue = request.form.get("cycleValue")
        zoneValue = request.form.get("zoneValue")  # escape the SQL values

        if seasonValue is None:
            seasonValue = ""
        if typeValue is None:
            typeValue = ""
        if cycleValue is None:
            cycleValue = ""
        if zoneValue is None:
            zoneValue = ""

        # if seasonValue == "%%" or typeValue == "%%" or cycleValue == "%%" or zoneValue == "%%":

        print(seasonValue, typeValue, cycleValue, zoneValue)
        with DBConfig.engine.begin() as conn:

            newSeason = '%%' + seasonValue + '%%'
            newType = '%%' + typeValue + '%%'
            newCycle = '%%' + cycleValue + '%%'
            newZone = '%%' + zoneValue + '%%'

            print(newSeason, newType, newCycle, newZone)

            plantnames = conn.execute("SELECT * from plant_information WHERE pref_season LIKE '{0}' "
                                      "AND plant_type LIKE '{1}' "
                                      "AND life_cycle LIKE '{2}' "
                                      "AND hardiness_zone LIKE '{3}'".format(newSeason, newType, newCycle, newZone))
        if plantnames.rowcount == 0:
            print("In the testing loop")
    return render_template('search.html', title='Plant Search', plantnames=plantnames)


# map page
@application.route('/map')
def plantmap():
    return render_template('map.html', title='Map')


# calendar page
@application.route('/calendar', methods=['GET', 'POST'])
def calendar():
    labels = []
    values = []
    seasonValue = ""
    typeValue = ""
    data = []
    plantnames = None
    with DBConfig.engine.begin() as conn:
        # initial load of all items in the database on the calendar
        plantnames = conn.execute("SELECT plant_name, pref_season_num1, pref_season_num2 FROM plant_information")
        for item in plantnames:
            labels.append('"' + item[0] + '",')
            values.append([item[1], item[2]])
    if request.method == 'POST':
        labels.clear()
        values.clear()

        seasonValue = request.form.get("seasonValue")
        typeValue = request.form.get("typeValue")

        if seasonValue is None or seasonValue == "*":
            seasonValue = ""
        if typeValue is None or typeValue == "*":
            typeValue = ""

        with DBConfig.engine.begin() as conn:

            newSeason = "%%" + seasonValue + "%%"
            newType = "%%" + typeValue + "%%"

            plantnames = conn.execute(
                "SELECT plant_name, pref_season_num1, pref_season_num2 FROM plant_information WHERE pref_season LIKE '{0}' AND plant_type LIKE '{1}'".format(
                    newSeason, newType))

            for item in plantnames:
                labels.append('"' + item[0] + '",')
                values.append([item[1], item[2]])
    return render_template('calendar.html', title='Planting Calendar', labels=labels, values=values)


# plant info page
# to link to individual plant item pages
# currently works when entering the url manually
# currently works by clicking the link in the catalog page
@application.route('/plantinfo/<plant_names>')
def plantinfo(plant_names):
    with DBConfig.engine.begin() as conn:
        plantnames = conn.execute("SELECT * FROM plant_information WHERE plant_name = '{0}'".format(plant_names))
    return render_template('plantinfo.html', plantnames=plantnames, plant_names=plant_names)


# takes the entered string from the search box in the navbar and parses against all columns in the
# database to find matching items
@application.route('/searchbar', methods=['GET', 'POST'])
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
                                      "OR maint_needs LIKE '{0}' OR soil_type LIKE '{0}' OR soil_ph LIKE '{0}' "
                                      "OR soil_drain LIKE '{0}' OR start_type LIKE '{0}' OR spacing_needs LIKE '{0}' "
                                      "OR grow_time_maturity LIKE '{0}' "
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


@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404 Error')


@application.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', title='Internal Server Error')


@application.route('/testing')
def testing():
    return render_template('testing.html')


@application.route('/healthcheck')
def healthcheck():
    return '', 200


if __name__ == '__main__':
    application.run(debug=True)
