from flask import Blueprint, request, jsonify, Response
from app.middlewares.AuthMiddleware import check_auth
from app.repositories.MongoRepository import MongoRepository
from jsonschema import validate
from bson import ObjectId
from bson.json_util import dumps
from app.utils.Roles import UserRole
from markupsafe import escape
from app.schemas.PostsSchemas import postsSchema, updatePostsSchema


posts = Blueprint('posts', __name__, url_prefix='/posts')

repo = MongoRepository('posts')
trainingRepo = MongoRepository('trainings')


@posts.route('/', methods=['GET'])
@check_auth(UserRole.USER)
def get_all():
    posts = repo.get_all()
    return Response(dumps(posts), mimetype='application/json'), 200


@posts.route('/<string:id>', methods=['GET'])
@check_auth(UserRole.USER)
def get_one(id):
    post = repo.get_one(id)

    if post is None:
        return jsonify({'error': 'Not found'}), 404
    
    training = trainingRepo.get_one(str(post['training_id']))

    post['training'] = training

    return Response(dumps(post), mimetype='application/json'), 200


@posts.route('/', methods=['POST'])
@check_auth(UserRole.USER)
def create():
    data = request.get_json()

    try:
        validate(instance=data, schema=postsSchema)
    except Exception as e:
        return jsonify({'error': 'Invalid data'}), 400
    

    if not trainingRepo.get_one(data['training_id']):
        return jsonify({'error': 'Training not found'}), 404

    post:dict ={
        "user_id": ObjectId(request.user_id),
        "training_id": data['training_id'],
        "content": escape(data['content']),
        "date": data['date'],
        "likes": 0,
        "comments": []
    }

    result = repo.insert(post).inserted_id

    return jsonify({'success': True, 'id': str(result)}), 201


@posts.route('/<string:id>', methods=['PUT'])
@check_auth(UserRole.USER)
def update(id):
    data = request.get_json()

    try:
        validate(instance=data, schema=updatePostsSchema)
    except Exception as e:
        return jsonify({'error': 'Invalid data'}), 400

    post = repo.get_one(id)

    if post is None:
        return jsonify({'error': 'Not found'}), 404
    
    if post['user_id'] != ObjectId(request.user_id):
        return jsonify({'error': 'Unauthorized'}), 401
    
    post['content'] = escape(data['content'])
    post['likes'] = data['likes']
    post['comments'] = data['comments']

    result = repo.update(id, post)

    if result.matched_count < 1:
        return jsonify({'error': 'Not found'}), 404

    return jsonify({'success': True}), 200


@posts.route('/<string:id>', methods=['DELETE'])
@check_auth(UserRole.USER)
def delete(id):
    post = repo.get_one(id)

    if post is None:
        return jsonify({'error': 'Not found'}), 404
    
    if post['user_id'] != ObjectId(request.user_id):
        return jsonify({'error': 'Unauthorized'}), 401
    
    result = repo.delete(id)

    if result.deleted_count < 1:
        return jsonify({'error': 'Not found'}), 404

    return jsonify({'success': True}), 200


