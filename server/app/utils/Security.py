from datetime import datetime, timedelta
import random
from config import Config
import jwt

class Security:

    def generate_token(user) -> str:
        payload = {
            'exp': datetime.now() + timedelta(hours=24),
            'id': user['_id'],
            'role': user['role'],
        }

        token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

        return token
    

    def decode_token(token) -> dict|None:
        try:
            decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            return decoded
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except Exception as e:
            return None

    def generate_verification_code() -> str:
        return str(random.randint(100000, 999999))