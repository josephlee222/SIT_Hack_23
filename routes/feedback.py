import shelve

from flask import Blueprint, render_template, request, flash, url_for, redirect

from forms import feedbackForm
from functions import loginAccess, adminAccess
from classes.Feedback import Feedback

feedback = Blueprint("feedback", __name__)


# @feedback.route('/feedback/feedback', methods=['GET', 'POST'])
# @loginAccess
# def feedbacklist():
#     with shelve.open()
@feedback.route('/connect/<id>/feedback', methods=['GET', 'POST'])
@loginAccess
def feedbacks(id):
    form = feedbackForm(request.form)
    if request.method == "POST" and form.validate():
        connect = {}
        try:
            with shelve.open("connections") as connections:
                connect = connections[id]

            if connect.status or connect.feedback:
                flash("Cannot give feedback yet or you already given a feedback previously", category="error")
                return redirect(url_for("connect.viewConnect"))

            feedback = Feedback(connect.userId, connect.councilId, form.q1.data, form.q2.data, form.experience_details.data, form.comments.data)

            with shelve.open("feedbacks") as feedbacks:
                feedbacks[str(feedback.id)] = feedback

            with shelve.open("connections") as connections:
                connections[id].feedback = True

            flash("Successfully given feedback to counsellor", category="success")
            return redirect(url_for("connect.viewConnect"))
        except KeyError:
            flash("Cannot find connection with provided ID to provide feedback", category="error")
            return redirect(url_for("connect.viewConnect"))
    else:
        try:
            with shelve.open("connections") as connections:
                if connections[id].status or connections[id].feedback:
                    flash("Cannot give feedback yet or you already given a feedback previously", category="error")
                    return redirect(url_for("connect.viewConnect"))

                return render_template("feedback/feedback.html", form=form)
        except KeyError:
            flash("Cannot find connection with provided ID to provide feedback", category="error")
            return redirect(url_for("connect.viewConnect"))
