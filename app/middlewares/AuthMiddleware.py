from functools import wraps
from flask import abort, request
import jwt
from config import Config

def check_auth(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                # Obtener el token JWT del encabezado de autorización
                token = request.headers['Authorization']
                token = token.split()[1]
                # Decodificar el token y obtener sus datos
                token_data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])

            except jwt.ExpiredSignatureError:
                abort(401)
            except jwt.InvalidTokenError:
                abort(401)
            except Exception as e:
                print(str(e))
                abort(401)

            # Verificar el rol del usuario
            if token_data['role'] > role:
                abort(401)

            # Agregar los datos del usuario al objeto de solicitud
            request.user_id = token_data['id']
            request.user_role = token_data['role']

            # Llamar a la función original con los argumentos originales
            return f(*args, **kwargs)

        return wrapper

    return decorator