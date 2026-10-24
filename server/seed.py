#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Workout, Exercise, WorkoutExercise


with app.app_context():

    print("Clearing existing data...")

    # Delete join records first because they contain foreign keys
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    db.session.commit()

    print("Creating exercises...")

    exercises = [
        Exercise(
            name="Push Ups",
            category="Strength",
            equipment_needed=False
        ),
        Exercise(
            name="Squats",
            category="Strength",
            equipment_needed=False
        ),
        Exercise(
            name="Running",
            category="Cardio",
            equipment_needed=False
        ),
        Exercise(
            name="Bench Press",
            category="Strength",
            equipment_needed=True
        ),
        Exercise(
            name="Plank",
            category="Core",
            equipment_needed=False
        )
    ]

    db.session.add_all(exercises)
    db.session.commit()

    print("Creating workouts...")

    workouts = [
        Workout(
            date=date(2026, 10, 24),
            duration_minutes=45,
            notes="Upper body strength training"
        ),
        Workout(
            date=date(2026, 10, 25),
            duration_minutes=30,
            notes="Cardio and endurance workout"
        ),
        Workout(
            date=date(2026, 10, 26),
            duration_minutes=60,
            notes="Full body strength workout"
        )
    ]

    db.session.add_all(workouts)
    db.session.commit()

    print("Linking exercises to workouts...")

    workout_exercises = [
        WorkoutExercise(
            workout_id=workouts[0].id,
            exercise_id=exercises[0].id,
            reps=15,
            sets=3
        ),
        WorkoutExercise(
            workout_id=workouts[0].id,
            exercise_id=exercises[3].id,
            reps=10,
            sets=4
        ),
        WorkoutExercise(
            workout_id=workouts[1].id,
            exercise_id=exercises[2].id,
            duration_seconds=1200
        ),
        WorkoutExercise(
            workout_id=workouts[2].id,
            exercise_id=exercises[1].id,
            reps=20,
            sets=3
        ),
        WorkoutExercise(
            workout_id=workouts[2].id,
            exercise_id=exercises[4].id,
            duration_seconds=60,
            sets=3
        )
    ]

    db.session.add_all(workout_exercises)
    db.session.commit()

    print("Database seeded successfully!")
    print(f"Exercises: {Exercise.query.count()}")
    print(f"Workouts: {Workout.query.count()}")
    print(f"Workout Exercises: {WorkoutExercise.query.count()}")
