from flask import Flask

# creating the flask app
app = Flask(__name__)


# setting the route for the pages
# index page
@app.route('/')
def index():
    return ("Testing")


@app.route('/about')
def about():
    return ("About Us...")


@app.route('/contact')
def contact():
    return ("Contact Us")


@app.route('/privacy')
def privacty():
    return ("Privacy Policy")


@app.route('/catalog')
def catalog():
    return ("Plant Index Page")


@app.route('/search')
def search():
    return ("Plant Search Page")


@app.route('/map')
def map():
    return ("Interactive Map Page")


@app.route('/plantinfo')
def plantinfo():
    return ("Individual Plant Info Page Holder")

# to run the application
if __name__ == "__main__":
    app.run(debug=True)
