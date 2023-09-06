import logging
import shelve
import smtplib
from datetime import datetime, timedelta

import jwt
from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from flask_mail import Message

import app
from classes.Feedback import Feedback
from forms import feedbackForm
from functions import flashFormErrors, goBack, loginAccess


feedback = Blueprint("feedback", __name__)

@feedback.route('/feedback/feedback/<id>', methods=['GET', 'POST'])
@loginAccess
def feedbacks(id):
    
    form = feedbackForm(request.form)
    if request.method == "POST" and form.validate():
        userDict = {}
        userDict = session["user"] 
        useremail = userDict['email']
        q1 = form.q1.data
        q2 = form.q2.data
        experience_details = form.experience_details.data
        comments = form.comments.data
        Feedback(useremail,id,q1,q2,experience_details,comments)

        with shelve.open("feedbacks") as feedback:
            feedback["feedback"] = Feedback
            flash("Feedback successfully sent!", category="success")

    return render_template("feedback/feedback.html", form=form)
