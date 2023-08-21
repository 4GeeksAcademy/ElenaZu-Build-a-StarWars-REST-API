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
from models import db, User, Character, Planet, Favorite
#from models import Person

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

@app.route('/user', methods=['GET'])
def get_users():

    users = User.query.all()
    response = list(map(lambda user: user.serialize(),users))
    return jsonify(response), 200


@app.route('/people', methods=['GET'])
def get_people():
    
    characters = Character.query.all()
    response = list(map(lambda character: character.serialize(),characters))
    return jsonify(response), 200


@app.route('/people/<int:character_id>',  methods=['GET'])
def get_character_by_id(character_id):

    character = Character.query.get(character_id)
    if not character:
         raise APIException("Character not found", status_code=404)
    return jsonify(character.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():

    planets = Planet.query.all()
    response = list(map(lambda planet: planet.serialize(),planets))
    return jsonify(response), 200

@app.route('/planets/<int:planet_id>',  methods=['GET'])
def get_planet_by_id(planet_id):

    planet = Planet.query.get(planet_id)
    if not planet:
         raise APIException("Planet not found", status_code=404)
    return jsonify(planet.serialize()), 200

@app.route('/user/favorites/<int:user_id>', methods=['GET'])
def get_users_favorite(user_id):
    user_id = 1;
    user_favorites = Favorite.query.filter_by(user_id = user_id).all()
    if not user_favorites:
        raise APIException("Favorite not found", status_code=400)
    response = list(map(lambda favorite: favorite.serialize(),user_favorites))
    return jsonify(response)


@app.route('/favorite/planet/<int:planet_id>',  methods=['POST'])
def add_new_favorite_planet(planet_id):

    current_user = 1
    planet = Planet.query.filter_by(id = planet_id).first()

    if planet is not None:
        favorite = Favorite.query.filter_by(name = planet.name).first()

        if favorite:
            return jsonify({"ok": True, "message": "El favorito existe"}), 200
        
        body = {
            "name" : planet.name, 
            "user_id" : current_user
        }
        new_favorite = Favorite.create(body)

        if new_favorite is not None:
            return jsonify(new_favorite.serialize()), 201
        
        return jsonify({"message": "Ocurrió un error del lado del servidor"}), 500
    
    return jsonify({
        "message": "Planeta no encontrado"
    }), 404 # No encontrado

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_new_favorite_character(character_id):

    current_user = 1
    character = Character.query.filter_by(id = character_id).first()
    
    if character:
        favorite = Favorite.query.filter_by(name = character.name).first() 

        if favorite:
            return jsonify({"ok": True, "message": "El favorito existe"}), 200

        body = {
            "name" : character.name, 
            "user_id" : current_user
        }
        new_favorite = Favorite.create(body)

        if new_favorite is not None:
            return jsonify(new_favorite.serialize()), 201
        
        return jsonify({"message": "El favorito no existe"}), 500
    
    return jsonify({
        "message": "Personaje no encontrado"
    }), 404

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):

    character = Character.query.filter_by(id = character_id).first()
    
    if character:

        Favorite.query.filter_by(name = character.name).first() 

        if favorite:

            character_deleted = Favorite.delete(favorite)

            return jsonify({"ok": True, "message": "El favorito se ha eliminado"}), 200
        
        return jsonify({"message": "El favorito no existe"}), 500
    
    return jsonify({"message": "Personaje no encontrado"}), 404

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):

    planet = Planet.query.filter_by(id = planet_id).first()
    
    if planet:

        favorite = Favorite.query.filter_by(name = planetgit .name).first() 

        if favorite:

            Favorite.delete(favorite)

            return jsonify({"ok": True, "message": "El favorito se ha eliminado"}), 200
        
        return jsonify({"message": "El favorito no existe"}), 500
    
    return jsonify({"message": "Personaje no encontrado"}), 404
        
    # planet = Planet.query.filter_by(id = planet_id).first()
    # if planet is not None:
    #     favorite = Favorite.query.filter_by(name = planet.name).first()
    #     if favorite:
    #         return jsonify({"ok": True, "message": "El favorito existe"}), 200
    #     new_favorite = Favorite(name =planet.name, user_id = current_user)
    #     try:
    #         db.session.add(new_favorite)
    #         db.session.commit()
    #         return jsonify(new_favorite.serialize()), 201 #se ha creado un recurso en la BD o en el servidor
    #     except Exception as error:
    #         db.session.rollback()
    #         return jsonify(error.args), 500 #Hubo un error del lado del servidor
    # return jsonify({
    #     "message": "Planeta no encontrado"
    # }), 404 # No encontrado



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
