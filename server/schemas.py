from marshmallow import (
    Schema,
    fields,
    validate,
    validates_schema,
    ValidationError
)

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)

    reps = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1)
    )
    sets = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1)
    )
    duration_seconds = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1)
    )

    @validates_schema
    def validate_exercise_details(self, data, **kwargs):
        if all(data.get(key) is None for key in (
            "reps", "sets", "duration_seconds"
        )):
            raise ValidationError(
                "Provide reps, sets, or duration_seconds."
            )


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )
    category = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50)
    )
    equipment_needed = fields.Bool(required=True)

    @validates_schema
    def validate_text(self, data, **kwargs):
        for key in ("name", "category"):
            if key in data and not data[key].strip():
                raise ValidationError(
                    {key: ["Cannot be blank."]}
                )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )
    notes = fields.Str(allow_none=True)


class WorkoutExerciseDetailSchema(WorkoutExerciseSchema):
    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutDetailSchema(WorkoutSchema):
    workout_exercises = fields.Nested(
        WorkoutExerciseDetailSchema,
        many=True,
        dump_only=True
    )


class WorkoutSummarySchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(dump_only=True)
    duration_minutes = fields.Int(dump_only=True)
    notes = fields.Str(dump_only=True)


class ExerciseWorkoutDetailSchema(WorkoutExerciseSchema):
    workout = fields.Nested(
        WorkoutSummarySchema,
        dump_only=True
    )


class ExerciseDetailSchema(ExerciseSchema):
    workout_exercises = fields.Nested(
        ExerciseWorkoutDetailSchema,
        many=True,
        dump_only=True
    )
