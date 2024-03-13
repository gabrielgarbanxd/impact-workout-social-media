from flask import Blueprint, request, jsonify, current_app
from app.repositories.MongoRepository import MongoRepository
from app.utils.Security import Security
from jsonschema import validate
from markupsafe import escape
from app.schemas.AuthSchemas import authEmailSchema, authUserNameSchema, authRegisterSchema
import bcrypt

auth = Blueprint('auth', __name__)

repo = MongoRepository('users')

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if 'email' in data:
        try:
            validate(instance=data, schema=authEmailSchema)
        except Exception as e:
            return jsonify({'error': 'Invalid email or password'}), 400
        
        user = repo.get_one_by('email', data['email'])

    elif 'username' in data:
        try:
            validate(instance=data, schema=authUserNameSchema)
        except Exception as e:
            return jsonify({'error': 'Invalid username or password'}), 400
        
        user = repo.get_one_by('username', data['username'])


    password = data['password']


    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({'error': 'Invalid credentials'}), 400
    
    user['_id'] = str(user['_id'])
    request.user_id = user['_id']
    
    encoded_token = Security.generate_token(user)

    return jsonify({'success': True, 'token': encoded_token, 'role': user['role']}), 200


@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    try:
        validate(instance=data, schema=authRegisterSchema)
    except Exception as e:
        return jsonify({'error': 'Invalid data'}), 400
    

    query = {'$or': [{'email': data['email']}, {'username': data['username']}]}

    if repo.count(query) > 0:
        return jsonify({'error': 'User already exists'}), 400

    
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    user: dict = {
        'username': escape(data['username']),
        'email': escape(data['email']),
        'password': hashed_password,
        'name': escape(data['name']),
        'role': data['role'],
        'gender': escape(data['gender']),
        'email_verified': False,
        'email_verification_code': Security.generate_verification_code()
    }
        

    result = repo.insert(user)

    user['_id'] = str(result.inserted_id)
    
    encoded_token = Security.generate_token(user)

    current_app.mail_sender.send_mail(user['email'], 'Email Verification', f'Your verification code is: {user["email_verification_code"]}')

    return jsonify({'success': True, 'token': encoded_token, 'role': user['role']}), 201


@auth.route('/verify-email-code', methods=['POST'])
def verify_email_code():
    data = request.get_json()

    if 'email' not in data or 'code' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    user = repo.get_one_by('email', data['email'])

    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    if 'email_verification_code' not in user:
        return jsonify({'error': 'User not found'}), 404
    
    if user['email_verification_code'] != data['code']:

        return jsonify({'error': 'Invalid code'}), 400
    
    repo.update(user['_id'], {'email_verified': True, 'email_verification_code': None})

    return jsonify({'success': True}), 200


@auth.route('/resend-verification-code', methods=['POST'])
def resend_verification_code():
    data = request.get_json()

    if 'email' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    user = repo.get_one_by('email', data['email'])

    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    if 'email_verification_code' not in user:
        return jsonify({'error': 'User not found'}), 404
    
    current_app.mail_sender.send_mail(user['email'], 'Email Verification', f'Your verification code is: {user["email_verification_code"]}')

    return jsonify({'success': True}), 200