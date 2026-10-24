from flask import Flask
from flask_migrate import Migrate
from models import db, Workout, Exercise, WorkoutExercise
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return {
        "message": "Welcome to the Workout API"
    }, 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)