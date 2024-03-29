from flask.ext.login import LoginManager
from models import User

#flask-login
login_manager = LoginManager()
login_manager.login_view = "login"
#login
@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)
