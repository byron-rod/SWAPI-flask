
from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User, Favorites, Planet, Character
from utils import APIException

api = Blueprint('api', __name__)


@api.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        if not data:
            raise APIException("Request body must be a JSON object", status_code=400)

        email = data.get("email")
        password = data.get("password")
        is_active = data.get("is_active")

        if not email or not password:
            raise APIException("Email and password are required", status_code=400)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            raise APIException("Email already in use", status_code=400)

        new_user = User(email=email, password=password, is_active=is_active)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@api.route('/planet', methods=['POST'])
def create_planet():
    try:
        data = request.get_json()

        if not data:
            raise APIException("Request body must be a JSON object", status_code=400)

        name = data.get("name")
        diameter = data.get("diameter")
        rotation_period = data.get("rotation_period")
        orbital_period = data.get("orbital_period")
        gravity = data.get("gravity")
        population = data.get("population")
        climate = data.get("climate")
        terrain = data.get("terrain")
        surface_water = data.get("surface_water")

        if not name:
            raise APIException("Planet name is required", status_code=400)

        existing_planet = Planet.query.filter_by(name=name).first()
        if existing_planet:
            raise APIException("Planet with this name already exists", status_code=400)

        new_planet = Planet(
            name=name,
            diameter=diameter,
            rotation_period=rotation_period,
            orbital_period=orbital_period,
            gravity=gravity,
            population=population,
            climate=climate,
            terrain=terrain,
            surface_water=surface_water
        )

        db.session.add(new_planet)
        db.session.commit()

        return jsonify({"message": "Planet created successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@api.route('/people', methods=['POST'])
def create_character():
    try:
        data = request.get_json()

        if not data:
            raise APIException("Request body must be a JSON object", status_code=400)

        name = data.get("name")
        birth_year = data.get("birth_year")
        eye_color = data.get("eye_color")
        gender = data.get("gender")
        hair_color = data.get("hair_color")
        height = data.get("height")
        skin_color = data.get("skin_color")
        homeworld = data.get("homeworld")
        species = data.get("species")

        if not name:
            raise APIException("Character name is required", status_code=400)

        existing_character = Character.query.filter_by(name=name).first()
        if existing_character:
            raise APIException("Character with this name already exists", status_code=400)

        new_character = Character(
            name=name,
            birth_year=birth_year,
            eye_color=eye_color,
            gender=gender,
            hair_color=hair_color,
            height=height,
            skin_color=skin_color,
            homeworld=homeworld,
            species=species
        )

        db.session.add(new_character)
        db.session.commit()

        return jsonify({"message": "Character created successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@api.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    try:
    
        favorites = Favorites.query.filter_by(user_id=user_id).all()
        favorites = list(map(lambda favorite: favorite.serialize(), favorites))

        return jsonify(favorites), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@api.route('/user/<int:user_id>/favorites', methods=['POST'])
def add_favorite(user_id):
    try:
        data = request.get_json()

        
        if not data:
            raise APIException("Request body must be a JSON object", status_code=400)

        planet_id = data.get("planet_id")
        character_id = data.get("character_id")

        if not planet_id and not character_id:
            raise APIException("Planet or character ID is required", status_code=400)

        
        existing_favorite = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id, character_id=character_id).first()
        if existing_favorite:
            raise APIException("Planet or character already in favorites", status_code=400)

        
        new_favorite = Favorites(
            user_id=user_id,
            planet_id=planet_id,
            character_id=character_id
        )

        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({"message": "Favorite created successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@api.route('/user/<int:user_id>/favorites/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(user_id, favorite_id):
    try:
        
        favorite = Favorites.query.filter_by(user_id=user_id, id=favorite_id).first()
        if not favorite:
            raise APIException("Favorite not found", status_code=404)

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"message": "Favorite deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@api.route('/user', methods=['GET'])
def get_users():
    try:
        
        users = User.query.all()

        serialized_users = [user.serialize() for user in users]

        return jsonify(serialized_users), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@api.route('/planet', methods=['GET'])
def get_planets():
    try:
        
        planets = Planet.query.all()

        
        serialized_planets = [planet.serialize() for planet in planets]

        return jsonify(serialized_planets), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@api.route('/people', methods=['GET'])
def get_characters():
    try:
        
        characters = Character.query.all()

        serialized_characters = [character.serialize() for character in characters]

        return jsonify(serialized_characters), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@api.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    try:
        planet = Planet.query.filter_by(id=planet_id).first()

        serialized_planet = planet.serialize()

        return jsonify(serialized_planet), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/people/<int:character_id>', methods=['GET'])
def get_character(character_id):
    try:
       
        character = Character.query.filter_by(id=character_id).first()

        serialized_character = character.serialize()

        return jsonify(serialized_character), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500  



