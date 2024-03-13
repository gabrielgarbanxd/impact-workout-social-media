from flask import Blueprint, request, jsonify, Response
from app.middlewares.AuthMiddleware import check_auth
from app.repositories.MongoRepository import MongoRepository
from app.schemas.TrainingSchema import trainingSchema
from jsonschema import validate
from bson import ObjectId
from bson.json_util import dumps
from app.utils.Roles import UserRole
from markupsafe import escape


trainings = Blueprint('trainings', __name__, url_prefix='/training-programs/<string:training_program_id>/trainings')

repo = MongoRepository('trainings')


@trainings.route('/', methods=['GET'])
@check_auth(UserRole.USER)
def get_all(training_program_id):
    
    query = {'training_program_id': ObjectId(training_program_id), 'user_id': ObjectId(request.user_id)}
    proyection = {'name': 1, 'date': 1, 'duration': 1, 'volume': 1, 'visibility': 1}


    trainings = repo.get_by_query_with_projection(query, proyection)

    return Response(dumps(trainings), mimetype='application/json'), 200


@trainings.route('/<string:id>', methods=['GET'])
@check_auth(UserRole.USER)
def get_one(training_program_id, id):
    training = repo.get_one(id)

    if training is None:
        return jsonify({'error': 'Not found'}), 404
    
    if training['user_id'] != ObjectId(request.user_id):
        return jsonify({'error': 'Unauthorized'}), 401

    return Response(dumps(training), mimetype='application/json'), 200


@trainings.route('/', methods=['POST'])
@check_auth(UserRole.USER)
def create(training_program_id):
    data = request.get_json()

    try:
        validate(instance=data, schema=trainingSchema)
    except Exception as e:
        return jsonify({'error': 'Invalid data'}), 400
    

    training:dict ={
        "date": data['date'],
        "duration": data['duration'],
        "volume": data['volume'],
        "reps": data['reps'],
        "sets": data['sets'],
        "exercises": data['exercises'],
        "image": data['image'],
        "description": escape(data['description']),
        "visibility": data['visibility'],
        "user_id": ObjectId(request.user_id),
        "training_program_id": ObjectId(training_program_id)
    }

    result = repo.insert(training).inserted_id

    return jsonify({'success': True, '_id': str(result)}), 201


@trainings.route('/<string:id>', methods=['PUT'])
@check_auth(UserRole.USER)
def update(training_program_id, id):
    data = request.get_json()

    try:
        validate(instance=data, schema=trainingSchema)
    except Exception as e:
        return jsonify({'error': 'Invalid data'}), 400

    training = repo.get_one(id)

    if training['user_id'] != ObjectId(request.user_id):
        return jsonify({'error': 'Unauthorized'}), 401

    training['date'] = data['date']
    training['duration'] = data['duration']
    training['volume'] = data['volume']
    training['reps'] = data['reps']
    training['sets'] = data['sets']
    training['exercises'] = data['exercises']
    training['image'] = data['image']
    training['description'] = escape(data['description'])
    training['visibility'] = data['visibility']

    repo.update(id, training)

    return jsonify({'success': True}), 200


@trainings.route('/<string:id>', methods=['DELETE'])
@check_auth(UserRole.USER)
def delete(training_program_id, id):
    training = repo.get_one(id)

    if training is None:
        return jsonify({'error': 'Not found'}), 404
    
    if training['user_id'] != ObjectId(request.user_id):
        return jsonify({'error': 'Unauthorized'}), 401
    
    repo.delete(id)

    return jsonify({'success': True}), 200


