from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField, validators


# contact us form
class ContactForm(FlaskForm):
    name = StringField("Name", [validators.InputRequired("Please enter your name.")])
    email = EmailField("Email", [validators.InputRequired("Please enter your email.")])
    subject = StringField("Subject", [validators.InputRequired("Please enter the message subject.")])
    message = TextAreaField("Message", [validators.InputRequired("Please enter a message.")])
    submit = SubmitField("Send")


# search form for use with the navbar
class SearchForm(FlaskForm):
    searchedPlant = StringField("Searched")
    submit = SubmitField("Submit")

