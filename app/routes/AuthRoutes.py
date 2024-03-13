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
    
    if user['email_verified'] == False:
        return jsonify({'error': 'Email not verified'}), 400
    
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
        'birthdate': data['birthdate'],
        'profile_picture': 'default.jpg',
        'bio': '',
        'links': {},
        'private': False,
        'vip': False,
        'followers': [],
        'body_measures': {},
        'training_programs': [],
        'following': [],
        'email_verified': False,
        'email_verification_code': Security.generate_verification_code()
    }
        

    result = repo.insert(user)

    user['_id'] = str(result.inserted_id)

    send_verification_email(user['email'], user['email_verification_code'], user['username'])

    return jsonify({'success': True}), 201


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
    

    user['_id'] = str(user['_id'])
    
    repo.update(user['_id'], {'email_verified': True, 'email_verification_code': None})

    encoded_token = Security.generate_token(user)

    return jsonify({'success': True, 'token': encoded_token, 'role': user['role']}), 200


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
    
    send_verification_email(user['email'], user['email_verification_code'], user['username'])

    return jsonify({'success': True}), 200


@auth.route('/forgot-password', methods=['POST'])
def forgot_password():
    pass


@auth.route('/reset-password', methods=['POST'])
def reset_password():
    pass




def send_verification_email(to, code, username):

    html = f'''
    <html lang="es">
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2>Verificación de Código</h2>
                <p>Estimado/a {username},</p>
                <p>Por favor, ingresa el siguiente código de verificación para completar el proceso:</p>
                <div style="background-color: #f4f4f4; padding: 10px; border-radius: 5px;">
                    <h3 style="margin: 0;">Código de Verificación:</h3>
                    <p style="font-size: 24px; font-weight: bold; margin: 10px 0; text-align: center;">{code}</p>
                </div>
            </div>
        </body>
    </html>
    '''


    current_app.mail_sender.send_mail(to, 'Email Verification', html, is_html=True)