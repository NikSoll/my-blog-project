from flask import request, jsonify, g
from . import auth_bp
from .shemas import UserRegisterSchema, UserLoginSchema, UserResponseSchema, TokenResponseSchema
from .service import AuthService
from app.core.secuirity import token_required


@auth_bp.route('/register', methods=['POST'])
def register():

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Нет данных'}), 400

        try:
            validated = UserRegisterSchema(**data)
        except Exception as e:
            return jsonify({'error': str(e)}), 400

        user, error = AuthService.register(validated.email, validated.password)

        if error:
            return jsonify({'error': error}), 400

        token = AuthService.generate_token(user)

        return jsonify({
            'success': True,
            'data': TokenResponseSchema(
                token=token,
                user=UserResponseSchema(
                    id=user.id,
                    email=user.email,
                    role=user.role
                ).dict()
            ).dict()
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Нет данных'}), 400

        try:
            validated = UserLoginSchema(**data)
        except Exception as e:
            return jsonify({'error': str(e)}), 400

        user, error = AuthService.login(validated.email, validated.password)

        if error:
            return jsonify({'error': error}), 401

        token = AuthService.generate_token(user)

        return jsonify({
            'success': True,
            'data': TokenResponseSchema(
                token=token,
                user=UserResponseSchema(
                    id=user.id,
                    email=user.email,
                    role=user.role
                ).dict()
            ).dict()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user():
    try:
        user = g.current_user
        return jsonify({
            'success': True,
            'data': UserResponseSchema(
                id=user.id,
                email=user.email,
                role=user.role
            ).dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500