from app.models import User
from app.extensions import db
import jwt
from datetime import datetime, timedelta
import os
from flask import current_app


class AuthService:

    @staticmethod
    def register(email, password):
        if User.query.filter_by(email=email).first():
            return None, "Пользователь с таким email уже существует"

        user = User(email=email)
        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()
            return user, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return None, "Неверный email или пароль"

        return user, None

    @staticmethod
    def generate_token(user):
        secret_key = os.getenv('JWT_SECRET_KEY', current_app.config.get('SECRET_KEY', 'secret'))

        payload = {
            'user_id': user.id,
            'email': user.email,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }

        token = jwt.encode(
            payload,
            secret_key,
            algorithm='HS256'
        )

        return token

    @staticmethod
    def decode_token(token):
        secret_key = os.getenv('JWT_SECRET_KEY', current_app.config.get('SECRET_KEY', 'secret'))

        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            return payload, None
        except jwt.ExpiredSignatureError:
            return None, "Токен истек"
        except jwt.InvalidTokenError:
            return None, "Неверный токен"