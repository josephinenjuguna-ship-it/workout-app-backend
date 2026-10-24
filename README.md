Workout Tracking API
A RESTful backend for personal trainers to create workouts, manage reusable exercises, and record sets, repetitions, and exercise duration. Built with Flask, Flask-SQLAlchemy, Flask-Migrate, and Marshmallow.
Features
- Create, list, view, and delete workouts and exercises.
- Assign an exercise to a workout with sets, reps, or duration.
- Reuse exercises across multiple workouts through the WorkoutExercise association model.
- Validate input with Marshmallow, SQLAlchemy model validators, and database constraints.
- Cascade deletion of associated workout-exercise records.
Tech stack
Python 3.8.13+, Flask 2.2.2, Flask-SQLAlchemy 3.0.3, Flask-Migrate 3.1.0, Marshmallow 3.20.1, SQLite, Pipenv, pytest.
Installation
git clone https://github.com/josephinenjuguna-ship-it/workout-app-backend.git
cd workout-app-backend
pipenv install --dev
pipenv shell
cd server
Replace YOUR-USERNAME with your GitHub username.
Database setup
Run these commands from server/:
flask --app app db upgrade
python seed.py
For a new project without an existing migrations/ directory, initialize and generate the first migration before upgrading:
flask --app app db init
flask --app app db migrate -m "Create workout tables"
flask --app app db upgrade
Note: python seed.py resets and replaces existing sample records. Do not use it on production data.
Run the API
From server/:
python app.py
The API is available at http://127.0.0.1:5555.
Endpoints
Method	Path	Description
GET	/workouts	List all workouts
GET	/workouts/<id>	View a workout and its exercises, including sets/reps/duration
POST	/workouts	Create a workout
DELETE	/workouts/<id>	Delete a workout and its associated join records
GET	/exercises	List all exercises
GET	/exercises/<id>	View an exercise and its associated workouts
POST	/exercises	Create an exercise
DELETE	/exercises/<id>	Delete an exercise and its associated join records
POST	/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises	Attach an exercise to a workout with reps, sets, or duration


Example: create a workout
curl -X POST http://127.0.0.1:5555/workouts \
  -H 'Content-Type: application/json' \
  -d '{"date":"2026-10-24","duration_minutes":45,"notes":"Strength training"}'
Example: create an exercise
curl -X POST http://127.0.0.1:5555/exercises \
  -H 'Content-Type: application/json' \
  -d '{"name":"Push Ups","category":"Strength","equipment_needed":false}'
Example: add an exercise to a workout
Replace 1 and 2 with existing workout and exercise IDs:
curl -X POST http://127.0.0.1:5555/workouts/1/exercises/2/workout_exercises \
  -H 'Content-Type: application/json' \
  -d '{"reps":12,"sets":3}'
Models and relationships
- Workout: id, date, duration_minutes, notes.
- Exercise: id, name, category, equipment_needed.
- WorkoutExercise: id, workout_id, exercise_id, reps, sets, duration_seconds.
A workout has many workout-exercise records; an exercise has many workout-exercise records. Together they form a many-to-many relationship between workouts and exercises.
Validation and errors
Examples of validation rules include positive workout duration, nonblank exercise name/category, and positive sets/reps/duration when provided. Invalid input returns HTTP 400; missing resources return HTTP 404. Successful creation returns HTTP 201, and successful deletion returns HTTP 204.
Run tests
From server/:
pipenv run python -m pytest tests/ -v
Project structure
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