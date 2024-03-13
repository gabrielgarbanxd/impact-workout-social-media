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
admin = Blueprint('admin', __name__, url_prefix='/admin')

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
    users = repo.get_all()
    users_list = [user for user in users]
    return jsonify(users_list), 200


@users.route('/<id>', methods=['GET'])
@check_auth(UserRole.USER)
def get_user(id):
    query = {'_id': id}
        
    projection = {
        '_id': 0,
        'username': 1,
        'email': 1,
        'name': 1,
        'gender': 1,
        'birthdate': 1,
        'profile_picture': 1,
        'bio': 1,
        'links': 1,
        'private': 1,
        'vip': 1,
        'followers': 1,
        'body_measures': 1,
        'training_programs': 1,
        'following': 1
    }    
    user = repo.get_by_query_with_projection(query=query, projection=projection)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return Response(dumps(user), status=200, mimetype='application/json')



# **** ADMIN *****

@admin.route('/me', methods=['GET'])
@check_auth(UserRole.USER)
def me():
    user = repo.get_one(request.user_id)
    return Response(dumps(user), mimetype='application/json')

@admin.route('/me', methods=['PUT'])
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

@admin.route('/me', methods=['DELETE'])
@check_auth(UserRole.USER)
def delete_me():
    repo.delete(request.user_id)
    return jsonify({'success': True}), 200

@admin.route('/', methods=['GET'])
@check_auth(UserRole.USER)
def get_users():
    users = repo.get_all()
    users_list = [user for user in users]
    return jsonify(users_list), 200

@admin.route('/<id>', methods=['GET'])
@check_auth(UserRole.USER)
def get_user(id):
    query = {'_id': id}  
    projection = {
        '_id': 0,
        'username': 1,
        'email': 1,
        'name': 1,
        'gender': 1,
        'birthdate': 1,
        'profile_picture': 1,
        'bio': 1,
        'links': 1,
        'private': 1,
        'vip': 1,
        'followers': 1,
        'body_measures': 1,
        'training_programs': 1,
        'following': 1
    }    
    user = repo.get_by_query_with_projection(query=query, projection=projection)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return Response(dumps(user), status=200, mimetype='application/json')


