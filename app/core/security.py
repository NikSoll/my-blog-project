from functools import wraps
from flask import request, jsonify, g
import jwt
import os


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'error': 'Токен не предоставлен'}), 401

        try:
            secret_key = os.getenv('JWT_SECRET_KEY', 'secret')
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])

            from app.models.user import User
            user = User.query.get(payload['user_id'])
            if not user:
                return jsonify({'error': 'Пользователь не найден'}), 401

            g.current_user = user

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Токен истек'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Неверный токен'}), 401

        return f(*args, **kwargs)

    return decorated

