from app.models import Post, User
from app.extensions import db
from datetime import datetime
from sqlalchemy import desc


class PostService:

    @staticmethod
    def get_all_posts():
        return Post.query.order_by(desc(Post.created_at)).all()

    @staticmethod
    def get_post_by_id(post_id):
        return Post.query.get(post_id)

    @staticmethod
    def create_post(title, body, user_id):
        post = Post(
            title=title,
            body=body,
            user_id=user_id
        )

        try:
            db.session.add(post)
            db.session.commit()
            return post, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def update_post(post, title=None, body=None):
        if title:
            post.title = title
        if body:
            post.body = body

        post.updated_at = datetime.utcnow()

        try:
            db.session.commit()
            return post, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def delete_post(post):
        try:
            db.session.delete(post)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def check_permission(post, user):
        return user.is_admin() or post.user_id == user.id