from flask import Flask, render_template

# creating the flask app
app = Flask(__name__)


# setting the route for the pages
# index page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/privacy')
def privacty():
    return render_template('privacy.html')


@app.route('/catalog')
def catalog():
    return render_template('catalog.html')


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/plantinfo')
def plantinfo():
    return render_template('plantinfo.html')


# to run the application
if __name__ == "__main__":
    app.run(debug=True)
