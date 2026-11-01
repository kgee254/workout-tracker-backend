from app import app
from extensions import db, bcrypt
from models import User, Workout


def seed_database():
    with app.app_context():
        # Remove existing sample data so the script can be rerun safely.
        Workout.query.delete()
        User.query.delete()

        # Create sample users with securely hashed passwords.
        user1 = User(
            username="kamau",
            password_hash=bcrypt.generate_password_hash("password123").decode("utf-8")
        )

        user2 = User(
            username="alex",
            password_hash=bcrypt.generate_password_hash("password456").decode("utf-8")
        )

        db.session.add_all([user1, user2])
        db.session.flush()

        # Create workouts belonging to the first user.
        workout1 = Workout(
            exercise="Push-ups",
            duration=15,
            notes="Three sets of push-ups",
            user_id=user1.id
        )

        workout2 = Workout(
            exercise="Running",
            duration=30,
            notes="Morning run",
            user_id=user1.id
        )

        # Create workouts belonging to the second user.
        workout3 = Workout(
            exercise="Squats",
            duration=20,
            notes="Bodyweight squats",
            user_id=user2.id
        )

        workout4 = Workout(
            exercise="Cycling",
            duration=45,
            notes="Evening cycling session",
            user_id=user2.id
        )

        db.session.add_all([workout1, workout2, workout3, workout4])
        db.session.commit()

        print("Database seeded successfully!")
        print(f"Users created: {User.query.count()}")
        print(f"Workouts created: {Workout.query.count()}")


if __name__ == "__main__":
    seed_database()