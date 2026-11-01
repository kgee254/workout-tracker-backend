import os

from flask import Flask
from flask_migrate import Migrate

from extensions import db, bcrypt, jwt
from models import User, Workout

from auth import auth_bp
from workouts import workouts_bp


def create_app():
    app = Flask(__name__)

    # Application configuration.
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///" + os.path.join(app.instance_path, "workout_tracker.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Replace this development key with a secure environment variable
    # before deploying the application.
    app.config["JWT_SECRET_KEY"] = os.environ.get(
        "JWT_SECRET_KEY",
        "development-only-change-this-key"
    )

    # Initialize extensions.
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(workouts_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)