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
from functions import flashFormErrors, goBack, loginAccess, adminAccess


feedback = Blueprint("feedback", __name__)

# @feedback.route('/feedback/feedback', methods=['GET', 'POST'])
# @loginAccess
# def feedbacklist():
#     with shelve.open()
@feedback.route('/feedback/feedback/<id>', methods=['GET', 'POST'])
@loginAccess
def feedbacks(id):
    userDict = {}
    userDict = session["user"] 
    useremail = userDict['email']

    with shelve.open("connections") as connections:
        
        for connection in connections:
            if connection.userId == useremail:
                if connection.feedback == True:
                    redirect(url_for("/"))
            
        form = feedbackForm(request.form)
        if request.method == "POST" and form.validate():
            
            q1 = form.q1.data
            q2 = form.q2.data
            experience_details = form.experience_details.data
            comments = form.comments.data
            Feedback(useremail,id,q1,q2,experience_details,comments)

            with shelve.open("feedbacks") as feedback:
                feedback["feedback"] = Feedback
            flash("Feedback successfully sent!", category="success")
        for connection in connections:
            if connection.userId == useremail:
                connection.feedback == True
                
    return render_template("feedback/feedback.html", form=form)


@feedback.route("/feedback/admin/<id>", methods=['GET', 'POST'])
@adminAccess
def viewAdminFeedback(id):  #id is admin id
    feedbackdb = []
    with shelve.open("feedbacks") as feedbacks:
        for feedback in feedbacks:
            if feedback["feedbacks"].get_counselloremail() == id:
                #only admin can check their own connections
                useremail = feedback.get_useremail()
                q1 = feedback.get_q1()
                q2 = feedback.get_q2()
                experience_details = feedback.get_experience_details()
                get_comments = feedback.get_comments()
                feedbackdb.append({"useremail": useremail,"q1":q1,"q2":q2,"experience_details":experience_details,"get_comments":get_comments})
    return render_template("feedback/feedbackAdmin.html" ,feedbackdb = feedbackdb)    #change it to the html

            

           