from datetime import datetime

from extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(128),
        nullable=False
    )

    # One user can own many workouts.
    workouts = db.relationship(
        "Workout",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)

    exercise = db.Column(
        db.String(120),
        nullable=False
    )

    duration = db.Column(
        db.Integer,
        nullable=False
    )

    notes = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Foreign key connecting the workout to its owner.
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="workouts"
    )