from flask import Blueprint, request, jsonify, Response
from app.middlewares.AuthMiddleware import check_auth
from app.repositories.MongoRepository import MongoRepository
from jsonschema import validate
from app.schemas.CustomExeciseSchema import customExerciseSchema
from bson import ObjectId
from bson.json_util import dumps
from app.utils.Roles import UserRole
from markupsafe import escape

exercises = Blueprint('exercises', __name__, url_prefix='/exercises')

repo = MongoRepository('exercises')


@exercises.route('/', methods=['GET'])
@check_auth(UserRole.USER)
def get_all():
    muscle = request.args.get('muscle')

    if muscle is not None:
        exercises = repo.get_by_query({'muscle': muscle})
    else:
        exercises = repo.get_all()

    return Response(dumps(exercises), mimetype='application/json'), 200


@exercises.route('/<string:id>', methods=['GET'])
@check_auth(UserRole.USER)
def get_one(id):
    exercise = repo.get_one(id)

    if exercise is None:
        return jsonify({'error': 'Not found'}), 404

    return Response(dumps(exercise), mimetype='application/json'), 200


@exercises.route('/', methods=['POST'])
@check_auth(UserRole.USER)
def create():
    data = request.get_json()

    try:
        validate(instance=data, schema=customExerciseSchema)
    except Exception as e:
        return jsonify({'error': 'Invalid data'}), 400

    user = repo.get_one(request.user_id)

    if user['vip'] == False:
        return jsonify({'error': 'Unauthorized'}), 401

    exercise: dict = {
        "name": escape(data['name']),
        "description": escape(data['description']) if 'description' in data else '',
        "category": escape(data['category']) if 'category' in data else '',
        "equipment": escape(data['equipment']) if 'equipment' in data else '',
        "muscle": escape(data['muscle']),
        "secondary_muscle": escape(data['secondary_muscle']) if 'secondary_muscle' in data else '',
        "video": escape(data['video']) if 'video' in data else '',
        "image": escape(data['image']) if 'image' in data else '',
        "custom": True
    }

    result = repo.insert(exercise).inserted_id

    return jsonify({'success': True, '_id': str(result)}), 201


@exercises.route('/<string:id>', methods=['PUT'])
@check_auth(UserRole.USER)
def update(id):
    data = request.get_json()

    try:
        validate(instance=data, schema=customExerciseSchema)
    except Exception as e:
        return jsonify({'error': 'Invalid data'}), 400

    user = repo.get_one(request.user_id)

    if user['vip'] == False:
        return jsonify({'error': 'Unauthorized'}), 401

    exercise = repo.get_one(id)

    if exercise is None or exercise['custom'] == False:
        return jsonify({'error': 'Not found'}), 404

    exercise['name'] = escape(data['name'])
    exercise['description'] = escape(data['description']) if 'description' in data else ''
    exercise['category'] = escape(data['category']) if 'category' in data else ''
    exercise['equipment'] = escape(data['equipment']) if 'equipment' in data else ''
    exercise['muscle'] = escape(data['muscle'])
    exercise['secondary_muscle'] = escape(data['secondary_muscle']) if 'secondary_muscle' in data else ''
    exercise['video'] = escape(data['video']) if 'video' in data else ''
    exercise['image'] = escape(data['image']) if 'image' in data else ''

    repo.update(id, exercise)

    return jsonify({'success': True}), 200


@exercises.route('/<string:id>', methods=['DELETE'])
@check_auth(UserRole.USER)
def delete(id):
    user = repo.get_one(request.user_id)

    if user['vip'] == False:
        return jsonify({'error': 'Unauthorized'}), 401

    exercise = repo.get_one(id)

    if exercise is None or exercise['custom'] == False:
        return jsonify({'error': 'Not found'}), 404

    repo.delete(id)

    return jsonify({'success': True}), 200