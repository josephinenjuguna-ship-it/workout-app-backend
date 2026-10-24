from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    __table_args__ = (
        CheckConstraint(
            'duration_minutes > 0',
            name='check_workout_duration'
        ),
    )

    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='workout',
        cascade='all, delete-orphan'
    )

    exercises = db.relationship(
        'Exercise',
        secondary='workout_exercises',
        viewonly=True
    )

    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if not isinstance(duration, int) or isinstance(duration, bool) or duration <= 0:
            raise ValueError('Workout duration must be a positive integer')
        return duration


class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='exercise',
        cascade='all, delete-orphan'
    )

    workouts = db.relationship(
        'Workout',
        secondary='workout_exercises',
        viewonly=True
    )

    @validates('name')
    def validate_name(self, key, name):
        if not isinstance(name, str) or len(name.strip()) < 2:
            raise ValueError('Exercise name must have at least 2 characters')
        return name.strip()

    @validates('category')
    def validate_category(self, key, category):
        if not isinstance(category, str) or not category.strip():
            raise ValueError('Exercise category cannot be empty')
        return category.strip()


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey('workouts.id'),
        nullable=False
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey('exercises.id'),
        nullable=False
    )

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    __table_args__ = (
        CheckConstraint(
            'reps IS NULL OR reps > 0',
            name='check_positive_reps'
        ),
        CheckConstraint(
            'sets IS NULL OR sets > 0',
            name='check_positive_sets'
        ),
        CheckConstraint(
            'duration_seconds IS NULL OR duration_seconds > 0',
            name='check_positive_seconds'
        ),
    )

    workout = db.relationship(
        'Workout',
        back_populates='workout_exercises'
    )

    exercise = db.relationship(
        'Exercise',
        back_populates='workout_exercises'
    )

    @validates('reps', 'sets', 'duration_seconds')
    def validate_positive_values(self, key, value):
        if value is not None:
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                raise ValueError(f'{key} must be a positive integer')
        return value
