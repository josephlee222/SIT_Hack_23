import shelve
from flask import flash, Blueprint, render_template, redirect, url_for, request
from functions import normalAccess, loginAccess, flashFormErrors, goBack
from classes.Connection import Connection
from forms import connectionForm

connect = Blueprint("connect", __name__)

@connect.route("/connect", methods=['GET', 'POST'])
@loginAccess
def viewConnect():
    form = connectionForm(request.form)

    if request.method == "POST" and form.validate():
        return
    else:
        userList = []
        deleteList = []
        with shelve.open("users") as users:
            userList = dict(users)

        with shelve.open("connections") as connections:
            for user in userList:
                count = 0
                if userList[user].accountType != "council":
                    deleteList.append(user)

                for connection in connections:
                    print(connection)
                    if connection.councilId == userList[user].id:
                        count += 1

                if count >= 3:
                    deleteList.append(user)

        for id in deleteList:
            userList.pop(id)

        print(userList)

        return render_template("connect/viewCouncils.html", userList=userList, form=form)
