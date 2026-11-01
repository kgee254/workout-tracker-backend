from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Shared extensions used throughout the application.
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()