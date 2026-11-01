from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import Workout

workouts_bp = Blueprint("workouts", __name__)


def workout_to_dict(workout):
    """Convert a workout into a JSON-serializable dictionary."""
    return {
        "id": workout.id,
        "exercise": workout.exercise,
        "duration": workout.duration,
        "notes": workout.notes,
        "created_at": workout.created_at.isoformat(),
        "user_id": workout.user_id
    }


def get_owned_workout(workout_id, user_id):
    """Find a workout only if it belongs to the authenticated user."""
    return Workout.query.filter_by(
        id=workout_id,
        user_id=user_id
    ).first()


@workouts_bp.route("/workouts", methods=["GET"])
@jwt_required()
def get_workouts():
    user_id = int(get_jwt_identity())

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    if page < 1 or per_page < 1:
        return jsonify({"error": "Page and per_page must be positive"}), 400

    # Limit page size to prevent excessively large responses.
    per_page = min(per_page, 100)

    pagination = Workout.query.filter_by(
        user_id=user_id
    ).order_by(
        Workout.id
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "workouts": [workout_to_dict(w) for w in pagination.items],
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages
        }
    }), 200


@workouts_bp.route("/workouts/<int:workout_id>", methods=["GET"])
@jwt_required()
def get_workout(workout_id):
    user_id = int(get_jwt_identity())
    workout = get_owned_workout(workout_id, user_id)

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    return jsonify(workout_to_dict(workout)), 200


@workouts_bp.route("/workouts", methods=["POST"])
@jwt_required()
def create_workout():
    data = request.get_json(silent=True) or {}

    exercise = data.get("exercise")
    duration = data.get("duration")
    notes = data.get("notes")

    if not isinstance(exercise, str) or not exercise.strip():
        return jsonify({"error": "Exercise is required"}), 400

    if isinstance(duration, bool) or not isinstance(duration, int) or duration <= 0:
        return jsonify({"error": "Duration must be a positive integer"}), 400

    user_id = int(get_jwt_identity())

    workout = Workout(
        exercise=exercise.strip(),
        duration=duration,
        notes=notes,
        user_id=user_id
    )

    db.session.add(workout)
    db.session.commit()

    return jsonify(workout_to_dict(workout)), 201


@workouts_bp.route("/workouts/<int:workout_id>", methods=["PATCH"])
@jwt_required()
def update_workout(workout_id):
    user_id = int(get_jwt_identity())
    workout = get_owned_workout(workout_id, user_id)

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({"error": "A JSON object with updates is required"}), 400

    if "exercise" in data:
        exercise = data["exercise"]

        if not isinstance(exercise, str) or not exercise.strip():
            return jsonify({"error": "Exercise cannot be empty"}), 400

        workout.exercise = exercise.strip()

    if "duration" in data:
        duration = data["duration"]

        if isinstance(duration, bool) or not isinstance(duration, int) or duration <= 0:
            return jsonify({"error": "Duration must be a positive integer"}), 400

        workout.duration = duration

    if "notes" in data:
        notes = data["notes"]

        if notes is not None and not isinstance(notes, str):
            return jsonify({"error": "Notes must be a string or null"}), 400

        workout.notes = notes

    db.session.commit()

    return jsonify(workout_to_dict(workout)), 200


@workouts_bp.route("/workouts/<int:workout_id>", methods=["DELETE"])
@jwt_required()
def delete_workout(workout_id):
    user_id = int(get_jwt_identity())
    workout = get_owned_workout(workout_id, user_id)

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    db.session.delete(workout)
    db.session.commit()

    return jsonify({"message": "Workout deleted successfully"}), 200