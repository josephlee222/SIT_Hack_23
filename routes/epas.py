import shelve
from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from classes.EPA import Epa
from functions import flashFormErrors

epas = Blueprint("epas", __name__)

@epas.route("/epas/", methods=['GET', 'POST'])
def viewEpas():
    with shelve.open("epas") as epas:
        return render_template("EPA/viewEpas.html", epas=epas)

@epas.route("/epas/<id>", methods=['GET', 'POST'])
def viewEpa(id):
    try:
        with shelve.open("epas", writeback=True) as epas:
            epasList = list(epas)
            current = epasList.index(id)
            return render_template("EPA/viewEpa.html", epa=epas[id], next=epasList[current + 1] if (current + 1) != len(
                epasList) else epasList[0], prev=epasList[current - 1])

    except KeyError:
        flash("PFA Certification does not exist.", category="error")
        return redirect(url_for("epas.viewEpas"))