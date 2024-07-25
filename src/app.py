"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Ships

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# my endpoints
@app.route('/users', methods=['GET'])
def get_all_users():

    results_query = User.query.all()
    results = list(map(lambda item: item.serialize(),results_query))

    response_body = {
        "msg": "All good",
        "results": results
    }

    return jsonify(response_body), 200

@app.route('/users/<int:id>', methods=['GET'])
def get_one_user(id):

    results_query = User.query.filter_by(id=id).first()

    response_body = {
        "msg": "All good",
        "results": results_query.serialize()
    }

    return jsonify(response_body), 200

@app.route('/characters', methods=['GET'])
def get_all_characters():

    results_query = Characters.query.all()
    results = list(map(lambda item: item.serialize(),results_query))

    response_body = {
        "msg": "All good",
        "results": results
    }

    return jsonify(response_body), 200

@app.route('/characters/<int:id>', methods=['GET'])
def get_one_character(id):

    results_query = Characters.query.filter_by(id=id).first()

    response_body = {
        "msg": "All good",
        "results": results_query.serialize()
    }

    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():

    results_query = Planets.query.all()
    results = list(map(lambda item: item.serialize(),results_query))

    response_body = {
        "msg": "All good",
        "results": results
    }

    return jsonify(response_body), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_one_planet(id):

    results_query = Planets.query.filter_by(id=id).first()

    response_body = {
        "msg": "All good",
        "results": results_query.serialize()
    }

    return jsonify(response_body), 200

@app.route('/ships', methods=['GET'])
def get_all_ships():

    results_query = Ships.query.all()
    results = list(map(lambda item: item.serialize(),results_query))

    response_body = {
        "msg": "All good",
        "results": results
    }

    return jsonify(response_body), 200

@app.route('/ships/<int:id>', methods=['GET'])
def get_one_ships(id):

    results_query = Ships.query.filter_by(id=id).first()

    response_body = {
        "msg": "All good",
        "results": results_query.serialize()
    }

    return jsonify(response_body), 200

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    fav_chars = user.fav_chars
    fav_planets = user.fav_planets
    fav_ships = user.fav_ships
    
    response = {
        "username": user.username,
        "favorite_characters": list(map(lambda item: item.name,fav_chars)),
        "favorite_planets": list(map(lambda item: item.name,fav_planets)),
        "favorite_ships": list(map(lambda item: item.name,fav_ships))
    }
    print(response)
    return jsonify(response)

@app.route('/users/<int:user_id>/add_fav_char/<int:char_id>', methods=['POST'])
def add_favorite_character(user_id, char_id):
    user = User.query.get(user_id)
    character = Characters.query.get(char_id)
    if not user or not character:
        return jsonify({"error": "User or Character not found"}), 404
    
    user.fav_chars.append(character)
    db.session.commit()
    
    return jsonify({"message": "Favorite character added"}), 200

@app.route('/users/<int:user_id>/add_fav_planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)
    if not user or not planet:
        return jsonify({"error": "User or Planet not found"}), 404
    
    user.fav_planets.append(planet)
    db.session.commit()
    
    return jsonify({"message": "Favorite planet added"}), 200

@app.route('/users/<int:user_id>/add_fav_ship/<int:ship_id>', methods=['POST'])
def add_favorite_ship(user_id, ship_id):
    user = User.query.get(user_id)
    ship = Ships.query.get(ship_id)
    if not user or not ship:
        return jsonify({"error": "User or Ship not found"}), 404
    
    user.fav_ships.append(ship)
    db.session.commit()
    
    return jsonify({"message": "Favorite ship added"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
