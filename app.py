import os
import shelve
from datetime import time, datetime

from dotenv.main import load_dotenv
from flask import Flask, render_template, session, url_for, make_response, send_from_directory
from flask_mail import Mail

from classes.User import User
from functions import normalAccess
from routes.adminUsers import adminUsers
from routes.adminEpas import adminEpas
from routes.adminBlog import adminBlog
from routes.blog import blogs
from routes.auth import auth
from routes.errors import errors
from routes.profile import profile
from routes.epas import epas
from routes.connect import connect
from routes.test import test
from routes.feedback import feedback

app = Flask(__name__)
app.secret_key = "aNDu7jhy1wKBP7y17j0o"
load_dotenv()

# Configuration
# The email error caused during the presentation is due to a send limit the account has reached
# I have implemented additional measures to handle the error
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ["MAIL_USERNAME"]
app.config['MAIL_PASSWORD'] = os.environ["MAIL_PASSWORD"]
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Register blueprints
app.register_blueprint(test)
app.register_blueprint(auth)
app.register_blueprint(adminUsers)
app.register_blueprint(adminEpas)
app.register_blueprint(adminBlog)
app.register_blueprint(blogs)
app.register_blueprint(connect)
app.register_blueprint(profile)
app.register_blueprint(epas)
app.register_blueprint(errors)
app.register_blueprint(feedback)


# ONLY HOMEPAGE HERE (Other pages please use separate files and link via blueprint)
@app.route('/')
@normalAccess
def home():
    session["previous_url"] = url_for("home")
    return render_template("home.html")

@app.route('/about')
@normalAccess
def about():
    return render_template("about.html")

@app.route('/sw.js')
def sw():
    response=make_response(send_from_directory('static', path='js/sw.js'))
    #change the content header file. Can also omit; flask will handle correctly.
    response.headers['Content-Type'] = 'application/javascript'
    return response

# Give website context
@app.context_processor
def websiteContextInit():

    return {
        "websiteName": "EasyAid",
        "now": datetime.now().date(),
    }

def initialization():
    print("Init code start")
    os.environ['TZ'] = 'Asia/Singapore'
    with shelve.open("data", writeback=True) as data:
        # Old products do not have product quantity, this updater on start will initialise the variable
        if "version" not in data:
            with shelve.open("products", writeback=True) as products:
                for product in products.values():
                    product.setQuantity(1)

            data["version"] = 2


        if "opening" not in data or "closing" not in data:
            print("No opening hours detected. Setting default 9am - 9pm opening hours.")
            data["opening"] = time(9, 0, 0)
            data["closing"] = time(21, 0, 0)

    with shelve.open("users", writeback=True) as users:
        if "admin@admin.com" not in users:
            print("Default admin user not detected. Creating one...")
            user = User("Admin", "Adminpassword", "admin@admin.com", "admin")
            users["admin@admin.com"] = user
            print("Default Admin E-mail: admin@admin.com")
            print("Default Admin Password: Adminpassword")

initialization()


if __name__ == '__main__':
    app.run(debug=True)