# Workout Tracking API

![Python](https://img.shields.io/badge/python-3.8.13%2B-blue)
![Flask](https://img.shields.io/badge/flask-2.2.2-black)
![Database](https://img.shields.io/badge/database-SQLite-lightgrey)
![Tests](https://img.shields.io/badge/tests-pytest-green)

A RESTful backend for personal trainers to create workouts, manage reusable exercises, and record sets, repetitions, and exercise duration.

Built with Flask, Flask-SQLAlchemy, Flask-Migrate, and Marshmallow.


## Features

- Create, list, view, and delete workouts and exercises.
- Assign an exercise to a workout with sets, reps, or duration.
- Reuse exercises across multiple workouts through the `WorkoutExercise` association model.
- Validate input with Marshmallow, SQLAlchemy model validators, and database constraints.
- Cascade deletion of associated workout-exercise records.

## Tech Stack

| Layer          | Tool                        |
| -------------- | --------------------------- |
| Language       | Python 3.8.13+              |
| Framework      | Flask 2.2.2                 |
| ORM            | Flask-SQLAlchemy 3.0.3      |
| Migrations     | Flask-Migrate 3.1.0         |
| Serialization  | Marshmallow 3.20.1          |
| Database       | SQLite                      |
| Dependencies   | Pipenv                      |
| Testing        | pytest                      |

## Prerequisites

- Python 3.8.13 or newer
- [Pipenv](https://pipenv.pypa.io/) (`pip install pipenv`)
- Git
- `curl` or a client such as Postman for trying the endpoints

## Installation

```bash
git clone https://github.com/josephinenjuguna-ship-it/workout-app-backend.git
cd workout-app-backend
pipenv install --dev
pipenv shell
cd server
```


## Database Setup

Run these commands from `server/`:

```bash
flask --app app db upgrade
python seed.py
```

For a new project without an existing `migrations/` directory, initialize and generate the first migration before upgrading:

```bash
flask --app app db init
flask --app app db migrate -m "Create workout tables"
flask --app app db upgrade
```

## Running the API

From `server/`:

```bash
python app.py
```

The API is available at `http://127.0.0.1:5555`.

## API Reference

| Method | Path                                                              | Description                                                        | Success |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------ | ------- |
| GET    | `/workouts`                                                       | List all workouts                                                  | 200     |
| GET    | `/workouts/<id>`                                                  | View a workout and its exercises, including sets/reps/duration     | 200     |
| POST   | `/workouts`                                                       | Create a workout                                                   | 201     |
| DELETE | `/workouts/<id>`                                                  | Delete a workout and its associated join records                   | 204     |
| GET    | `/exercises`                                                      | List all exercises                                                 | 200     |
| GET    | `/exercises/<id>`                                                 | View an exercise and its associated workouts                       | 200     |
| POST   | `/exercises`                                                      | Create an exercise                                                 | 201     |
| DELETE | `/exercises/<id>`                                                 | Delete an exercise and its associated join records                 | 204     |
| POST   | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Attach an exercise to a workout with reps, sets, or duration       | 201     |

### Request Bodies

**POST `/workouts`**

| Field              | Type    | Required | Notes                          |
| ------------------ | ------- | -------- | ------------------------------ |
| `date`             | string  | Yes      | ISO format, e.g. `2026-10-24`  |
| `duration_minutes` | integer | Yes      | Must be positive               |
| `notes`            | string  | No       | Free text                      |

**POST `/exercises`**

| Field              | Type    | Required | Notes                |
| ------------------ | ------- | -------- | -------------------- |
| `name`             | string  | Yes      | Must not be blank    |
| `category`         | string  | Yes      | Must not be blank    |
| `equipment_needed` | boolean | No       | Whether gear is used |

**POST `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`**

| Field              | Type    | Required | Notes                           |
| ------------------ | ------- | -------- | ------------------------------- |
| `reps`             | integer | No       | Positive when provided          |
| `sets`             | integer | No       | Positive when provided          |
| `duration_seconds` | integer | No       | Positive when provided          |

## Usage Examples

### Create a workout

```bash
curl -X POST http://127.0.0.1:5555/workouts \
  -H 'Content-Type: application/json' \
  -d '{"date":"2026-10-24","duration_minutes":45,"notes":"Strength training"}'
```

### Create an exercise

```bash
curl -X POST http://127.0.0.1:5555/exercises \
  -H 'Content-Type: application/json' \
  -d '{"name":"Push Ups","category":"Strength","equipment_needed":false}'
```

### Add an exercise to a workout

Replace `1` and `2` with existing workout and exercise IDs:

```bash
curl -X POST http://127.0.0.1:5555/workouts/1/exercises/2/workout_exercises \
  -H 'Content-Type: application/json' \
  -d '{"reps":12,"sets":3}'
```

### View a workout with its exercises

```bash
curl http://127.0.0.1:5555/workouts/1
```

### Delete a workout

```bash
curl -X DELETE http://127.0.0.1:5555/workouts/1
```

## Data Models

| Model             | Fields                                                                |
| ----------------- | --------------------------------------------------------------------- |
| `Workout`         | `id`, `date`, `duration_minutes`, `notes`                             |
| `Exercise`        | `id`, `name`, `category`, `equipment_needed`                          |
| `WorkoutExercise` | `id`, `workout_id`, `exercise_id`, `reps`, `sets`, `duration_seconds` |

A workout has many workout-exercise records; an exercise has many workout-exercise records. Together they form a many-to-many relationship between workouts and exercises.

```
Workout 1 ──< WorkoutExercise >── 1 Exercise
```

Deleting a workout or an exercise also deletes its `WorkoutExercise` records.

## Validation and Errors

Input is validated in three layers: Marshmallow schemas, SQLAlchemy model validators, and database constraints.

Examples of validation rules:

- Workout duration must be positive.
- Exercise name and category must not be blank.
- Sets, reps, and duration must be positive when provided.

| Status | Meaning                                  |
| ------ | ---------------------------------------- |
| 200    | Request succeeded                        |
| 201    | Resource created                         |
| 204    | Resource deleted (no response body)      |
| 400    | Invalid input                            |
| 404    | Resource not found                       |

## Running Tests

From `server/`:

```bash
pipenv run python -m pytest tests/ -v
```

## Project Structure

```
workout-app-backend/
├── server/
│   ├── app.py            # Flask app and routes
│   ├── models.py         # SQLAlchemy models and validators
│   ├── schemas.py        # Marshmallow schemas
│   ├── seed.py           # Sample data (resets existing records)
│   ├── migrations/       # Flask-Migrate files
│   └── tests/
│       └── test_app.py
├── Pipfile
├── Pipfile.lock
├── README.md
└── .gitignore
```

## Troubleshooting

| Problem                                   | Fix                                                                                   |
| ----------------------------------------- | ------------------------------------------------------------------------------------- |
| `flask: command not found`                | Run `pipenv shell` first, or prefix commands with `pipenv run`.                       |
| `no such table` errors                    | Run `flask --app app db upgrade` from `server/`.                                      |
| Port 5555 already in use                  | Stop the other process, or change the port in `app.py`.                               |
| Seed data missing or unexpected           | Re-run `python seed.py` (this wipes existing sample records).                         |
| Tests fail on import                      | Run pytest from `server/` so the app modules resolve.                                 |

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Make your changes and add tests.
4. Run `pipenv run python -m pytest tests/ -v` and confirm everything passes.
5. Commit, push, and open a pull request.