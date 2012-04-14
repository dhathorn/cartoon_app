#imports
#from contextlib import closing
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from login_manager import login_manager
from models import db

#config
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('DELAY_SETTINGS', silent=True)
#app.secret_key = '\xe3\xc4\xc0%c\xe6\xc1\x87\x11:k\xc574P\x93s\x0c!\xb2-&\xbbs'
db.init_app(app)
login_manager.setup_app(app)

import cartoon_app.views
