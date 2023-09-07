import shelve

from flask import flash, Blueprint, render_template, redirect, url_for, request, session

from classes.Connection import Connection
from classes.Message import Message
from forms import connectionForm, chatForm
from functions import loginAccess
from app import socketio
from flask_socketio import join_room, emit, send

connect = Blueprint("connect", __name__)


@socketio.on("room")
def handleJoinConnection(data):
    join_room(data["roomId"])
    print("New user joined room " + str(data["roomId"]))
    send('User has entered the room.', to=data["roomId"])

@connect.route("/connect", methods=['GET', 'POST'])
@loginAccess
def viewConnect():
    if session["user"]["accountType"] == "council":
        # Get current chats
        connectionList = []
        with shelve.open("connections") as connections:
            for connection in connections:
                if connections[connection].councilId == session["user"]["email"] and connections[connection].status:
                    connectionList.append(connections[connection])

        return render_template("connect/viewConnections.html", connections=connectionList)
    else:
        userList = []
        deleteList = []
        active = False
        connect = ""
        with shelve.open("users") as users:
            userList = dict(users)

        with shelve.open("connections") as connections:
            for user in userList:
                count = 0
                if userList[user].accountType != "council":
                    print("delete because non-counsellor")
                    deleteList.append(user)

                for connection in connections:
                    print(connection)
                    if connections[connection].councilId == userList[user].email and connections[connection].status:
                        count += 1

                    if connections[connection].userId == session["user"]["email"] and connections[connection].status:
                        active = True
                        connect = connections[connection]

                if count >= 3:
                    print("delete because reach maximum")
                    deleteList.append(user)

        for id in deleteList:
            userList.pop(id)

        print(userList)

        return render_template("connect/viewCouncils.html", userList=userList, active=active,
                               connection=connect)


@connect.route("/connect/<id>", methods=['GET', 'POST'])
@loginAccess
def connectDetails(id):
    user = ""
    count = 0
    form = connectionForm(request.form)

    if request.method == "POST" and form.validate():
        connect = Connection(session["user"]["email"], form.councilId.data, session["user"]["nickname"])
        # NEED TO CHANGE TO NICKNAME!!! (Done)
        message = Message(session["user"]["email"], connect.id, form.message.data, session["user"]["nickname"])

        with shelve.open("connections") as connections:
            connections[str(connect.id)] = connect

        with shelve.open("messages") as messages:
            messages[str(message.id)] = message

        flash("Conversation successfully created.", category="success")
        return redirect(url_for("connect.viewConnect"))
    else:
        try:
            with shelve.open("users") as users:
                user = users[id]

            with shelve.open("connections") as connections:
                for connection in connections:
                    if connections[connection].councilId == user.email and connections[connection].status:
                        count += 1

                    if connections[connection].userId == session["user"]["email"] and connections[connection].status:
                        flash("Cannot show counsellor details. You are already having a session", category="error")
                        return redirect(url_for("connect.viewConnect"))

                if count >= 3:
                    flash("Cannot show counsellor details. Counsellor has reached maximum active chats",
                          category="error")
                    return redirect(url_for("connect.viewConnect"))

                form.councilId.data = user.email
                return render_template("connect/viewCouncil.html", user=user, count=count, form=form)

        except KeyError:
            flash("Cannot show counsellor details. User does not exist", category="error")
            return redirect(url_for("connect.viewConnect"))


@connect.route("/connect/chat/<id>", methods=['GET', 'POST'])
@loginAccess
def chatroom(id):
    form = chatForm(request.form)
    messageList = []
    connect = ""
    counsellor = ""
    user = ""
    if request.method == "POST" and form.validate():
        # Create a new chat message
        message = Message(session["user"]["email"], id, form.message.data, session["user"]["nickname"])
        with shelve.open("messages") as messages:
            messages[str(message.id)] = message
        socketio.emit("chat", {
            "nickname": message.nickname,
            "message": message.message
        }, to=int(id))
    try:
        with shelve.open("connections") as connections:
            connect = connections[id]

        if not connect.status:
            flash("This connection is not active anymore.", category="error")
            return redirect(url_for("connect.viewConnect"))

        if connect.userId != session["user"]["email"] and connect.councilId != session["user"]["email"]:
            flash("Not allowed to view this chat.", category="error")
            return redirect(url_for("connect.viewConnect"))

        with shelve.open("users") as users:
            counsellor = users[connect.councilId]
            user = users[connect.userId]

        with shelve.open("messages") as messages:
            for message in messages:
                print(messages[message].userId, session["user"]["email"])
                if messages[message].connectionId == int(id):
                    print("A")
                    messageList.append(messages[message])

        form.connectionId.data = id
        print(messageList)
        return render_template("connect/chatroom.html", user=user, counsellor=counsellor, messages=messageList,
                               connect=connect, form=form)
    except KeyError:
        flash("Cannot find connection with provided ID", category="error")
        return redirect(url_for("connect.viewConnect"))

