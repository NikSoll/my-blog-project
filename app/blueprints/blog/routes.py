from flask import request, jsonify, g
from . import blog_bp
from .schemas import PostCreateSchema, PostUpdateSchema, PostResponseSchema, PostListResponseSchema
from .service import PostService
from app.core.decorators import token_required
from app.models import Post


@blog_bp.route('/', methods=['GET'])
def get_posts():
    try:
        posts = PostService.get_all_posts()

        posts_data = []
        for post in posts:
            posts_data.append(PostResponseSchema(
                id=post.id,
                title=post.title,
                body=post.body,
                author_id=post.user_id,
                author_email=post.author.email,
                created_at=post.created_at,
                updated_at=post.updated_at
            ).dict())

        return jsonify({
            'success': True,
            'data': PostListResponseSchema(
                posts=posts_data,
                total=len(posts_data)
            ).dict()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@blog_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    try:
        post = PostService.get_post_by_id(post_id)

        if not post:
            return jsonify({'error': 'Пост не найден'}), 404

        return jsonify({
            'success': True,
            'data': PostResponseSchema(
                id=post.id,
                title=post.title,
                body=post.body,
                author_id=post.user_id,
                author_email=post.author.email,
                created_at=post.created_at,
                updated_at=post.updated_at
            ).dict()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@blog_bp.route('/', methods=['POST'])
@token_required
def create_post():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Нет данных'}), 400

        try:
            validated = PostCreateSchema(**data)
        except Exception as e:
            return jsonify({'error': str(e)}), 400

        post, error = PostService.create_post(
            title=validated.title,
            body=validated.body,
            user_id=g.current_user.id
        )

        if error:
            return jsonify({'error': error}), 400

        return jsonify({
            'success': True,
            'message': 'Пост успешно создан',
            'data': {
                'id': post.id,
                'title': post.title
            }
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@blog_bp.route('/<int:post_id>', methods=['PUT'])
@token_required
def update_post(post_id):
    try:
        post = PostService.get_post_by_id(post_id)
        if not post:
            return jsonify({'error': 'Пост не найден'}), 404

        if not PostService.check_permission(post, g.current_user):
            return jsonify({'error': 'Нет прав для редактирования этого поста'}), 403

        data = request.get_json()
        if not data:
            return jsonify({'error': 'Нет данных'}), 400

        try:
            validated = PostUpdateSchema(**data)
        except Exception as e:
            return jsonify({'error': str(e)}), 400

        updated_post, error = PostService.update_post(
            post=post,
            title=validated.title,
            body=validated.body
        )

        if error:
            return jsonify({'error': error}), 400

        return jsonify({
            'success': True,
            'message': 'Пост успешно обновлен',
            'data': {
                'id': updated_post.id,
                'title': updated_post.title
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@blog_bp.route('/<int:post_id>', methods=['DELETE'])
@token_required
def delete_post(post_id):
    try:
        post = PostService.get_post_by_id(post_id)
        if not post:
            return jsonify({'error': 'Пост не найден'}), 404

        if not PostService.check_permission(post, g.current_user):
            return jsonify({'error': 'Нет прав для удаления этого поста'}), 403

        success, error = PostService.delete_post(post)

        if error:
            return jsonify({'error': error}), 400

        return jsonify({
            'success': True,
            'message': 'Пост успешно удален'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500