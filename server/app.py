from flask import Flask, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from models import db, Workout, Exercise, WorkoutExercise
from schemas import (
    WorkoutSchema,
    WorkoutDetailSchema,
    ExerciseSchema,
    ExerciseDetailSchema,
    WorkoutExerciseSchema,
    WorkoutExerciseDetailSchema
)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

workout_schema = WorkoutSchema()
exercise_schema = ExerciseSchema()
workout_exercise_schema = WorkoutExerciseSchema()


@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify({"errors": error.messages}), 400


@app.errorhandler(ValueError)
def handle_value_error(error):
    db.session.rollback()
    return jsonify({"error": str(error)}), 400


@app.errorhandler(IntegrityError)
def handle_integrity_error(error):
    db.session.rollback()
    return jsonify({
        "error": "Database constraint violated."
    }), 400


@app.errorhandler(SQLAlchemyError)
def handle_database_error(error):
    db.session.rollback()
    return jsonify({
        "error": "A database error occurred."
    }), 500


@app.route('/')
def index():
    return jsonify({
        "message": "Welcome to the Workout API"
    }), 200



@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()

    return jsonify(
        workout_schema.dump(workouts, many=True)
    ), 200



@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = db.session.get(Workout, id)

    if workout is None:
        return jsonify({
            "error": "Workout not found"
        }), 404

    return jsonify(
        WorkoutDetailSchema().dump(workout)
    ), 200



@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "A JSON object is required"
        }), 400

    validated = workout_schema.load(data)

    workout = Workout(**validated)

    db.session.add(workout)
    db.session.commit()

    return jsonify(
        workout_schema.dump(workout)
    ), 201



@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)

    if workout is None:
        return jsonify({
            "error": "Workout not found"
        }), 404

    db.session.delete(workout)
    db.session.commit()

    return '', 204



@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()

    return jsonify(
        exercise_schema.dump(exercises, many=True)
    ), 200



@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)

    if exercise is None:
        return jsonify({
            "error": "Exercise not found"
        }), 404

    return jsonify(
        ExerciseDetailSchema().dump(exercise)
    ), 200



@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "A JSON object is required"
        }), 400

    validated = exercise_schema.load(data)

    exercise = Exercise(**validated)

    db.session.add(exercise)
    db.session.commit()

    return jsonify(
        exercise_schema.dump(exercise)
    ), 201



@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)

    if exercise is None:
        return jsonify({
            "error": "Exercise not found"
        }), 404

    db.session.delete(exercise)
    db.session.commit()

    return '', 204



@app.route(
    '/workouts/<int:workout_id>/exercises/'
    '<int:exercise_id>/workout_exercises',
    methods=['POST']
)
def add_exercise_to_workout(workout_id, exercise_id):

    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if workout is None or exercise is None:
        return jsonify({
            "error": "Workout or exercise not found"
        }), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "A JSON object is required"
        }), 400

    validated = workout_exercise_schema.load(data)

    workout_exercise = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        **validated
    )

    db.session.add(workout_exercise)
    db.session.commit()

    return jsonify(
        WorkoutExerciseDetailSchema().dump(
            workout_exercise
        )
    ), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)