import logging
import shelve
import smtplib
from datetime import datetime, timedelta

import jwt
from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from flask_mail import Message

import app
from classes.User import User
from forms import feedbackForm
from functions import flashFormErrors, goBack, loginAccess


feedback = Blueprint("feedback", __name__)

@feedback.route('/feedback/feedback', methods=['GET', 'POST'])
@loginAccess
def feedbacks():
    print("here")
    form = feedbackForm(request.form)
    if request.method == "POST" and form.validate():
        userDict = {}
        userDict = session["user"] 
        email = userDict.email
        experience_details = form.experience_details.data
        comments = form.comments.data

        with shelve.open("feedbacks") as feedback:
            with shelve.open("users") as users:
                pass
    return render_template("feedback/feedback.html", form=form)
