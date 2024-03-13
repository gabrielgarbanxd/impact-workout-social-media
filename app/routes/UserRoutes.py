import bcrypt
from flask import Blueprint, request, jsonify, Response
from bson.json_util import dumps
from app.repositories.MongoRepository import MongoRepository
from jsonschema import validate
from markupsafe import escape
from app.schemas.UserSchemas import userSchema
from app.middlewares.AuthMiddleware import check_auth
from app.utils.Roles import UserRole

users = Blueprint('users', __name__, url_prefix='/users')
adminUsers = Blueprint('admin', __name__, url_prefix='/admin/users')

repo = MongoRepository('users')

@users.route('/me', methods=['GET'])
@check_auth(UserRole.USER)
def me():
    user = repo.get_one(request.user_id)

    return Response(dumps(user), mimetype='application/json')



@users.route('/me', methods=['PUT'])
@check_auth(UserRole.USER)
def update_me():
    data = request.get_json()

    try:
        validate(instance=data, schema=userSchema)
    except Exception as e:
        return jsonify({'error': 'Invalid data'}), 400

    user = repo.get_one(request.user_id)

    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    user['username'] = escape(data['username'])
    user['email'] = escape(data['email'])
    user['password'] = hashed_password
    user['name'] = escape(data['name'])
    user['gender'] = data['gender']
    user['birthdate'] = data['birthdate']
    user['profile_picture'] = escape(data['profile_picture'])
    user['bio'] = escape(data['bio'])
    user['links'] = data['links']
    user['private'] = data['private']
    user['vip'] = data['vip']
    user['followers'] = data['followers']
    user['body_measures'] = data['body_measures']
    user['training_programs'] = data['training_programs']
    user['following'] = data['following']

    repo.update(request.user_id, user)

    return jsonify({'success': True}), 200


@users.route('/me', methods=['DELETE'])
@check_auth(UserRole.USER)
def delete_me():
    repo.delete(request.user_id)

    return jsonify({'success': True}), 200


@users.route('/', methods=['GET'])
@check_auth(UserRole.USER)
def get_users():
    # solo se devuelven los usuarios que no son privados, y solo se devuelven los campos necesarios (username, profile_picture)
    users = repo.get_by_query_with_projection({'private': False}, {'username': 1, 'profile_picture': 1})

    return Response(dumps(users), status=200, mimetype='application/json')


@users.route('/<string:id>', methods=['GET'])
@check_auth(UserRole.USER)
def get_user(id):
    
    user = repo.get_one(id)
    
    if not user or user['private']:
        return jsonify({'error': 'User not found'}), 404
    
    return Response(dumps(user), status=200, mimetype='application/json')



# **** ADMIN *****


@adminUsers.route('/', methods=['GET'])
@check_auth(UserRole.ADMIN)
def get_users():
    users = repo.get_all()

    return Response(dumps(users), status=200, mimetype='application/json')


@adminUsers.route('/<string:id>', methods=['GET'])
@check_auth(UserRole.ADMIN)
def get_user(id):
    user = repo.get_one(id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return Response(dumps(user), status=200, mimetype='application/json')



@adminUsers.route('/<string:id>', methods=['DELETE'])
@check_auth(UserRole.ADMIN)
def delete_user(id):
    repo.delete(id)

    return jsonify({'success': True}), 200




