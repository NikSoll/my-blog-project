from app.extensions import db
from datetime import datetime
from passlib.hash import bcrypt


class User(db.Model):
    __tablename__ = 'users'
#основа
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    bio = db.Column(db.Text, nullable=True)
#ава
    avatar_url = db.Column(db.String(500), nullable=True)
    avatar_path = db.Column(db.String(500), nullable=True)
    avatar_thumb_url = db.Column(db.String(500), nullable=True)
#время
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
#статус
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_banned = db.Column(db.Boolean, default=False)
#настройки
    email_notifications = db.Column(db.Boolean, default=True)
    theme_preference = db.Column(db.String(20), default='light')
#связи
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = None
    likes = db.relationship('Like', backref='user', lazy='dynamic')

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.set_password(password)
#хеш пароль
    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)
#валид пароль
    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)
#адм
    def is_admin(self):
        return self.role == 'admin'
#модерат
    def is_moderator(self):
        return self.role in ['admin', 'moderator']
#обновление врем вход
    def update_last_login(self):
        self.last_login = datetime.utcnow()
        db.session.commit()
#удал польз
    def soft_delete(self):
        self.deleted_at = datetime.utcnow()
        self.is_active = False
        db.session.commit()
#вост польз
    def restore(self):
        self.deleted_at = None
        self.is_active = True
        db.session.commit()
#бан
    def ban(self):
        self.is_banned = True
        self.is_active = False
        db.session.commit()
#разбан
    def unban(self):
        self.is_banned = False
        self.is_active = True
        db.session.commit()
#обновление авы
    def update_avatar(self, avatar_url=None, avatar_path=None, avatar_thumb_url=None):
        if avatar_url:
            self.avatar_url = avatar_url
        if avatar_path:
            self.avatar_path = avatar_path
        if avatar_thumb_url:
            self.avatar_thumb_url = avatar_thumb_url
        db.session.commit()
#удаление авы
    def remove_avatar(self):
        self.avatar_url = None
        self.avatar_path = None
        self.avatar_thumb_url = None
        db.session.commit()
#словарь для апи
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'role': self.role,
            'bio': self.bio,
            'avatar_url': self.avatar_url,
            'avatar_thumb_url': self.avatar_thumb_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_verified': self.is_verified,
            'posts_count': self.posts.count() if self.posts else 0,
            'comments_count': self.comments.count() if self.comments else 0,
            'likes_count': self.liked_posts.count() if self.liked_posts else 0
        }

    def to_public_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'bio': self.bio,
            'avatar_url': self.avatar_url,
            'avatar_thumb_url': self.avatar_thumb_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'role': self.role,
            'posts_count': self.posts.count() if self.posts else 0
        }

    def __repr__(self):
        return f'<User {self.username}>'