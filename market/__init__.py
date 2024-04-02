from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()# To create databases 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db' #dictionary that accepts new values from us
#To make the info given by user secure by secret key
app.config['SECRET_KEY']='b9148c8daf50de651e347075'
app.app_context().push()

bcrypt = Bcrypt(app) #To store passwords as hash passwords
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = 'info'
db.init_app(app)

from market import routes