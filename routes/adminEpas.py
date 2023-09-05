import shelve
from flask import flash, Blueprint, render_template, request, session, redirect, url_for
from classes.EPA import Epa
from forms import addEpaForm
from functions import flashFormErrors, adminAccess

adminEpas = Blueprint("adminEpas", __name__)

@adminEpas.route("/admin/epas/", methods=['GET', 'POST'])
@adminAccess
def viewAllEpas():
    with shelve.open("epas") as epas:
        return render_template("admin/EPA/viewEpas.html", epas=epas)

@adminEpas.route("/admin/epas/add", methods=['GET', 'POST'])
def addEpa():
    form = addEpaForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        description = form.description.data
        duration = form.duration.data
        mode = form.mode.data
        location = form.location.data

        epa = Epa(name, description, location, duration, mode)

        with shelve.open("epas") as epas:
            epas[str(epa.id)] = epa
            flash("EPA successfully created", category="success")
            redirect("adminEpas.viewAllEpas")
    else:
        flashFormErrors("Unable to create the EPA", form.errors)

    return render_template("admin/EPA/addEpa.html", form=form)
