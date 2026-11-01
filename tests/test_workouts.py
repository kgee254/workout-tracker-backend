def test_create_workout(client, auth_headers):
    response = client.post(
        "/workouts",
        headers=auth_headers,
        json={
            "exercise": "Push-ups",
            "duration": 15,
            "notes": "Three sets",
        },
    )

    assert response.status_code == 201
    assert response.get_json()["exercise"] == "Push-ups"


def test_workouts_require_authentication(client):
    response = client.get("/workouts")

    assert response.status_code == 401


def test_list_workouts(client, auth_headers):
    client.post(
        "/workouts",
        headers=auth_headers,
        json={"exercise": "Running", "duration": 30},
    )

    response = client.get("/workouts", headers=auth_headers)

    assert response.status_code == 200
    assert len(response.get_json()["workouts"]) == 1


def test_update_workout(client, auth_headers):
    created = client.post(
        "/workouts",
        headers=auth_headers,
        json={"exercise": "Squats", "duration": 10},
    )
    workout_id = created.get_json()["id"]

    response = client.patch(
        f"/workouts/{workout_id}",
        headers=auth_headers,
        json={"duration": 20},
    )

    assert response.status_code == 200
    assert response.get_json()["duration"] == 20


def test_delete_workout(client, auth_headers):
    created = client.post(
        "/workouts",
        headers=auth_headers,
        json={"exercise": "Cycling", "duration": 30},
    )
    workout_id = created.get_json()["id"]

    response = client.delete(
        f"/workouts/{workout_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200


def test_user_cannot_access_another_users_workout(client, auth_headers):
    from extensions import db, bcrypt
    from models import User, Workout

    with client.application.app_context():
        other_user = User(
            username="anotheruser",
            password_hash=bcrypt.generate_password_hash(
                "password456"
            ).decode("utf-8"),
        )
        db.session.add(other_user)
        db.session.commit()

        workout = Workout(
            exercise="Private workout",
            duration=20,
            user_id=other_user.id,
        )
        db.session.add(workout)
        db.session.commit()
        workout_id = workout.id

    response = client.get(
        f"/workouts/{workout_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404