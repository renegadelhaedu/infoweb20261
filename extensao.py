from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#instanciar o objeto do login manager
login_manager = LoginManager()
bd = SQLAlchemy()
