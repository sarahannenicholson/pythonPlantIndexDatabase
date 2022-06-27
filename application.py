from flask import Flask, render_template, request
import pymysql

# instance identifer - plant-index-database
# username - admin
# pw - admin123
# port - 3306
# hostname - plant-index-database.cyaimo2g0lsu.us-east-2.rds.amazonaws.com


# creating the flask application
application = Flask(__name__)

db = pymysql.connect(host='plant-index-database.cyaimo2g0lsu.us-east-2.rds.amazonaws.com', user='admin',
                     password='admin123')

cursor = db.cursor()


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
    sql = 'use plant_database'
    cursor.execute(sql)
    cursor.execute("SELECT plant_name FROM plant_information")
    data = cursor.fetchall()
    return render_template('catalog.html', data=data)


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
@application.route('/plantinfo/<plant_name>', methods=['GET', 'POST'])
def plantinfo(plant_name):
    sql = 'use plant_database'
    cursor.execute(sql)
    sql2 = 'SELECT * FROM plant_information WHERE plant_name = plant_name'
    cursor.execute(sql2)

    if plant_name in 'testing':
        return 'success'

    return render_template('plantinfo.html', plant_name=plant_name)


# testing page to make sure the db connection is working
# currently uses secondary template to add names to a random table on the database to check import works
@application.route('/testing', methods=['GET', 'POST'])
def testing():
    if request.method == "POST":
        sql = 'use testing'
        cursor.execute(sql)
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        cursor.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
        cursor.connection.commit()
        return 'success'
    return render_template('testing.html')


@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@application.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')


# to run the application
if __name__ == "__main__":
    application.run(debug=True)
