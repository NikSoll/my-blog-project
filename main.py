from flask import Flask, g, request
from dotenv import load_dotenv
import os
import jwt

load_dotenv()


def create_app(config_name='default'):
    app = Flask(__name__)

    from app.config import config
    app.config.from_object(config.get(config_name, config['default']))

    from app.extensions import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    try:
        from app.blueprints.main import main_bp
        app.register_blueprint(main_bp)
    except ImportError as e:
        print(f"main_bp not found: {e}")

    try:
        from app.blueprints.auth import auth_bp
        app.register_blueprint(auth_bp)
    except ImportError as e:
        print(f"auth_bp not found: {e}")

    try:
        from app.api.v1 import api_v1_bp
        app.register_blueprint(api_v1_bp)
    except ImportError as e:
        print(f"api_v1_bp not found: {e}")

    @app.before_request
    def load_current_user():
        token = None
        auth_header = request.headers.get('Authorization')
        print(f"Auth header: {auth_header}")

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            print(f"Token: {token[:20]}...")
        if token:
            try:
                secret_key = os.getenv('JWT_SECRET_KEY', app.config.get('SECRET_KEY', 'secret'))
                payload = jwt.decode(token, secret_key, algorithms=['HS256'])
                print(f"Payload: {payload}")

                from app.models.user import User
                user = User.query.get(payload['user_id'])
                print(f"User found: {user}")

                g.current_user = user
            except Exception as e:
                print(f"Error loading user: {e}")
                g.current_user = None
        else:
            g.current_user = None
            print("No token found")

    return app




app = create_app()

if __name__ == '__main__':
    app.run(debug=True)