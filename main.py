from app import app, socketio, initialization

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

initialization()
if __name__ == '__main__':
    app.debug = True
    socketio.run(debug=True)