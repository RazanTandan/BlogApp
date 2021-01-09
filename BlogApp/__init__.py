from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)	
app.config['SECRET_KEY'] = '716151ecd8eb81be790673124d56cfdf08'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'users.login' # redirect to login page if unauthorization happens
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'rajantandan24@gmail.com'
app.config['MAIL_PASSWORD'] = 'Rajan1722'
mail = Mail(app)


from BlogApp.main.routes import main  
from BlogApp.posts.routes import posts
from BlogApp.users.routes import users
from BlogApp.errors.handlers import errors

app.register_blueprint(main)
app.register_blueprint(posts)
app.register_blueprint(users)
app.register_blueprint(errors)