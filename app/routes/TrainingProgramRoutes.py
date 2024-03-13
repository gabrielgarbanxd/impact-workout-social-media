from flask import Blueprint, request, jsonify, Response
from app.middlewares.AuthMiddleware import check_auth
from app.repositories.MongoRepository import MongoRepository
from app.schemas.TrainingProgramSchemas import trainingProgramSchema
from jsonschema import validate
from bson import ObjectId
from bson.json_util import dumps
from app.utils.Roles import UserRole
from markupsafe import escape

trainingPrograms = Blueprint('trainingPrograms', __name__, url_prefix='/training-programs')

repo = MongoRepository('training_programs')

@trainingPrograms.route('/', methods=['GET'])
@check_auth(UserRole.USER)
def get_all():
    training_programs = repo.get_by_query_with_projection({'user_id': ObjectId(request.user_id)}, {'name': 1})
    return Response(dumps(training_programs), mimetype='application/json'), 200


@trainingPrograms.route('/<string:id>', methods=['GET'])
@check_auth(UserRole.USER)
def get_one(id):
    training_program = repo.get_one(id)

    if training_program is None:
        return jsonify({'error': 'Not found'}), 404
    
    if training_program['user_id'] != ObjectId(request.user_id):
        return jsonify({'error': 'Unauthorized'}), 401

    return Response(dumps(training_program), mimetype='application/json'), 200


@trainingPrograms.route('/', methods=['POST'])
@check_auth(UserRole.USER)
def create():
    data = request.get_json()

    try:
        validate(instance=data, schema=trainingProgramSchema)
    except Exception as e:
        return jsonify({'error': 'Invalid data'}), 400

    data['user_id'] = ObjectId(request.user_id)

    result = repo.insert(data).inserted_id

    return jsonify({'success': True, '_id': str(result)}), 201


@trainingPrograms.route('/<string:id>', methods=['PUT'])
@check_auth(UserRole.USER)
def update(id):
    data = request.get_json()

    try:
        validate(instance=data, schema=trainingProgramSchema)
    except Exception as e:
        return jsonify({'error': 'Invalid data'}), 400

    training_program = repo.get_one(id)

    if training_program is None:
        return jsonify({'error': 'Not found'}), 404
    
    if training_program['user_id'] != ObjectId(request.user_id):
        return jsonify({'error': 'Unauthorized'}), 401
    

    for key in data:
        if key != 'user_id' and key != '_id' and key != 'created_at' and training_program.get(key) is not None:
            training_program[key] = data[key]

    repo.update(id, training_program)

    return jsonify({'success': True}), 200



@trainingPrograms.route('/<string:id>', methods=['DELETE'])
@check_auth(UserRole.USER)
def delete(id):
    training_program = repo.get_one(id)

    if training_program is None:
        return jsonify({'error': 'Not found'}), 404
    
    if training_program['user_id'] != ObjectId(request.user_id):
        return jsonify({'error': 'Unauthorized'}), 401

    repo.delete(id)

    return jsonify({'success': True}), 200
