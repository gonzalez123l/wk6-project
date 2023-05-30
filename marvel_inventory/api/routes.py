from flask import Blueprint, request, jsonify
from marvel_inventory.helpers import token_required
from marvel_inventory.models import db, Character, character_schema, characters_schema

api = Blueprint('api', __name__, url_prefix='/api')
#Create Car Endpoint

@api.route('/getdata')
@token_required
def getdata():
    return {'some':'value'}

@api.route('/characters', methods=['POST'])
@token_required
def create_character(our_user):
    name = request.json['name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_power = request.json['super_power']
    user_token = our_user.token

    character = Character(name, description, comics_appeared_in, super_power, user_token=user_token)
    db.session.add(character)
    db.session.commit()

    response = character_schema.dump(character)

    return jsonify(response)

# RETRIEVE(READ) ALL CARs ENDPOINT
@api.route('/characters', methods=['GET'])
@token_required
def get_characters(our_user):
    owner = our_user.token
    characters = Character.query.filter_by(user_token=owner).all()
    response = characters_schema.dump(characters)

    return jsonify(response)

#Reteieve Car by id endpoint
@api.route('/characters/<id>', methods=['GET'])
@token_required
def get_character(our_user, id):
    if id:
        character = Character.query.get(id)
        response = character_schema.dump(character)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid ID required'}), 401

# UPDATE Car ENDPOINT
@api.route('/characters/<id>', methods=['PUT'])
@token_required
def update_character(our_user, id):
    character = Character.query.get(id)

    character.name = request.json['name']
    character.description = request.json['description']
    character.comics_appeared_in = request.json['comics_appeared_in']
    character.super_power = request.json['super_power']
    character.user_token = our_user.token

    db.session.commit()

    response = character_schema.dump(character)

    return jsonify(response)

# DELETE Car ENDPOINT
@api.route('/characters/<id>', methods=['DELETE'])
@token_required
def delete_character(our_user, id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()

    response = character_schema.dump(character)

    return jsonify(response)