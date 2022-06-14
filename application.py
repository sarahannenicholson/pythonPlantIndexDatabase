from flask import Flask, render_template

# creating the flask application
application = Flask(__name__)


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
@application.route('/catalog')
def catalog():
    return render_template('catalog.html')


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
@application.route('/plantinfo')
def plantinfo():
    return render_template('plantinfo.html')


@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@application.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')


# to run the application
if __name__ == "__main__":
    application.run(debug=True)
