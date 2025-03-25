# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(jsonify(body), 200)


@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    try:
        earthquake = db.session.get(Earthquake, id)  
        
        if earthquake:
            return make_response(jsonify({
                "id": earthquake.id,
                "magnitude": earthquake.magnitude,
                "location": earthquake.location,
                "year": earthquake.year
            }), 200)
        else:
            return make_response(jsonify({"message": f"Earthquake {id} not found."}), 404)
    
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    if earthquakes:
        return make_response(jsonify({
            "count": len(earthquakes),
            "quakes": [
                {
                    "id": quake.id,
                    "location": quake.location,
                    "magnitude": quake.magnitude,
                    "year": quake.year
                }
                for quake in earthquakes
            ]
        }), 200)
    else:
        return make_response(jsonify({"count": 0, "quakes": []}), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
