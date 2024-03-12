from datetime import datetime, timedelta

from bson import ObjectId
from config import Config
import jwt

from app.repositories.MongoRepository import MongoRepository

class Security:

    # Constructor, puede recibir el repositorio de usuarios como argumento
    def __init__(self):
        pass

    def generate_token(self, user) -> str:
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=1),
            'id': user['_id'],
            'role': user['role'],
        }

        token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

        return token
    
    def revoke_token(self, user_id) -> None:
        pass