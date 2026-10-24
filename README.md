# Workout Tracking API

## Project Description

The Workout Tracking API is a RESTful backend application built using Python, Flask, Flask-SQLAlchemy, and Marshmallow.

The application allows personal trainers to create, view, and delete workouts and exercises. Trainers can also associate reusable exercises with workouts while recording sets, repetitions, and exercise duration.

The project demonstrates RESTful API development, database relationships, data validation, serialization, database migrations, and automated testing.

## Technologies Used

- Python 3.8.13+
- Flask 2.2.2
- Flask-SQLAlchemy 3.0.3
- Flask-Migrate 3.1.0
- Marshmallow 3.20.1
- SQLite
- Pipenv
- Pytest
- Git and GitHub

## Project Structure

```text
workout-app-backend/
├── server/
│   ├── app.py
│   ├── models.py
│   ├── schemas.py
│   ├── seed.py
│   ├── migrations/
│   └── tests/
│       └── test_app.py
├── Pipfile
├── Pipfile.lock
├── README.md
└── .gitignore
```

## Installation Instructions

### 1. Clone the repository

```bash
git clone https://github.com/josephinenjuguna-ship-it/workout-app-backend.git
cd workout-app-backend
```


### 2. Install dependencies

Ensure Python and Pipenv are installed.

```bash
pipenv install 
```

### 3. Activate the virtual environment

```bash
pipenv shell
```

### 4. Navigate to the server directory

```bash
cd server
```

Apply existing database migrations:

```bash
flask --app app db upgrade
```

When making future model changes, generate a migration before upgrading:

```bash
flask --app app db migrate -m "Update database models"
flask --app app db upgrade
```

### 5. Seed the database

```bash
python seed.py
```

The seed script creates example workouts, exercises, and workout-exercise associations.

It also clears existing sample data before inserting fresh records.

## Running the Application

From the `server` directory, run:

```bash
flask --app app run --debug --port 5555
```

The API will be available at:

`http://127.0.0.1:5555`

## Database Models

### Workout

Stores workout information.

| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| date | Date | Workout date |
| duration_minutes | Integer | Total workout duration |
| notes | Text | Optional workout notes |

### Exercise

Stores reusable exercise information.

| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| name | String | Exercise name |
| category | String | Exercise category |
| equipment_needed | Boolean | Whether equipment is required |

### WorkoutExercise

Connects workouts and exercises.

| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| workout_id | Integer | Foreign key to Workout |
| exercise_id | Integer | Foreign key to Exercise |
| reps | Integer | Number of repetitions |
| sets | Integer | Number of sets |
| duration_seconds | Integer | Exercise duration in seconds |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/workouts` | Retrieve all workouts |
| GET | `/workouts/<id>` | Retrieve a workout and its exercises |
| POST | `/workouts` | Create a new workout |
| DELETE | `/workouts/<id>` | Delete a workout |
| GET | `/exercises` | Retrieve all exercises |
| GET | `/exercises/<id>` | Retrieve an exercise and its workouts |
| POST | `/exercises` | Create a new exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout with sets, reps, or duration |

### Example: Create a Workout

**POST** `/workouts`

Request body:

```json
{
  "date": "2026-10-24",
  "duration_minutes": 45,
  "notes": "Upper body strength training"
}
```

Expected status: `201 Created`

### Example: Create an Exercise

**POST** `/exercises`

Request body:

```json
{
  "name": "Push Ups",
  "category": "Strength",
  "equipment_needed": false
}
```

Expected status: `201 Created`

### Example: Add an Exercise to a Workout

**POST** `/workouts/1/exercises/1/workout_exercises`

Request body:

```json
{
  "reps": 15,
  "sets": 3
}
```

Expected status: `201 Created`

## Data Validation

The application implements validation at three levels.

**Database constraints**
- Workout duration must be positive.
- Exercise repetitions and sets must be positive when provided.
- Required