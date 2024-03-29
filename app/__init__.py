from flask import Flask
from flask_bootstrap import Bootstrap 
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()
db = SQLAlchemy()
from flask_uploads import UploadSet,configure_uploads,IMAGES
photos = UploadSet('photos',IMAGES)
mail = Mail()

def create_app(config_name):
  app = Flask(__name__)

  from . main import main as main_blueprint
  app.register_blueprint(main_blueprint)


  #creating the app configurations
  app.config.from_object(config_options[config_name])

  # Initializing flask extensions
  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint,url_prefix = '/authenticate')
  bootstrap.init_app(app)
  db.init_app(app)
  login_manager.init_app(app)
  mail = Mail()
  
  # setting config
  from .requests import configure_request
  configure_request(app)

  #configure uploaset 
  configure_uploads(app,photos)

  return app