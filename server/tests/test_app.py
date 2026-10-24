import pytest
from datetime import date

from app import app
from models import db, Workout, Exercise, WorkoutExercise


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with app.app_context():
        original_engine = db.engines[None]
        from sqlalchemy.pool import StaticPool
        from sqlalchemy import create_engine

        test_engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool
        )

        db.engines[None] = test_engine
        db.create_all()

        with app.test_client() as test_client:
            yield test_client

        db.session.remove()
        db.drop_all()
        db.engines[None] = original_engine
        test_engine.dispose()


def create_workout(client):
    response = client.post("/workouts", json={
        "date": "2026-10-24",
        "duration_minutes": 45,
        "notes": "Strength training"
    })
    assert response.status_code == 201
    return response.get_json()["id"]


def create_exercise(client):
    response = client.post("/exercises", json={
        "name": "Push Ups",
        "category": "Strength",
        "equipment_needed": False
    })
    assert response.status_code == 201
    return response.get_json()["id"]


def test_get_workouts(client):
    response = client.get("/workouts")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_workout(client):
    workout_id = create_workout(client)

    response = client.get(f"/workouts/{workout_id}")

    assert response.status_code == 200
    assert response.get_json()["duration_minutes"] == 45


def test_invalid_workout_duration(client):
    response = client.post("/workouts", json={
        "date": "2026-10-24",
        "duration_minutes": -10
    })

    assert response.status_code == 400
    assert "duration_minutes" in response.get_json()["errors"]


def test_get_missing_workout(client):
    response = client.get("/workouts/999")
    assert response.status_code == 404


def test_delete_workout(client):
    workout_id = create_workout(client)

    response = client.delete(f"/workouts/{workout_id}")

    assert response.status_code == 204
    assert client.get(f"/workouts/{workout_id}").status_code == 404


def test_get_exercises(client):
    response = client.get("/exercises")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_exercise(client):
    exercise_id = create_exercise(client)

    response = client.get(f"/exercises/{exercise_id}")

    assert response.status_code == 200
    assert response.get_json()["name"] == "Push Ups"


def test_invalid_exercise_name(client):
    response = client.post("/exercises", json={
        "name": "",
        "category": "Strength",
        "equipment_needed": False
    })

    assert response.status_code == 400


def test_get_missing_exercise(client):
    response = client.get("/exercises/999")
    assert response.status_code == 404


def test_delete_exercise(client):
    exercise_id = create_exercise(client)

    response = client.delete(f"/exercises/{exercise_id}")

    assert response.status_code == 204
    assert client.get(f"/exercises/{exercise_id}").status_code == 404


def test_add_exercise_to_workout(client):
    workout_id = create_workout(client)
    exercise_id = create_exercise(client)

    response = client.post(
        f"/workouts/{workout_id}/exercises/"
        f"{exercise_id}/workout_exercises",
        json={
            "reps": 15,
            "sets": 3
        }
    )

    assert response.status_code == 201

    data = response.get_json()
    assert data["reps"] == 15
    assert data["sets"] == 3

    workout_response = client.get(f"/workouts/{workout_id}")
    workout_data = workout_response.get_json()

    assert len(workout_data["workout_exercises"]) == 1


def test_invalid_workout_exercise(client):
    workout_id = create_workout(client)
    exercise_id = create_exercise(client)

    response = client.post(
        f"/workouts/{workout_id}/exercises/"
        f"{exercise_id}/workout_exercises",
        json={
            "reps": -5,
            "sets": 0
        }
    )

    assert response.status_code == 400


def test_delete_workout_cascades(client):
    workout_id = create_workout(client)
    exercise_id = create_exercise(client)

    client.post(
        f"/workouts/{workout_id}/exercises/"
        f"{exercise_id}/workout_exercises",
        json={"reps": 10, "sets": 3}
    )

    response = client.delete(f"/workouts/{workout_id}")

    assert response.status_code == 204

    with app.app_context():
        assert WorkoutExercise.query.count() == 0