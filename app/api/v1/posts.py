from flask import jsonify, request, g
from app.core.decorators import token_required
from app.models.post import Post
from app.models.like import Like
from app.extensions import db
from . import api_v1_bp


@api_v1_bp.route('/post', methods=['GET'])
def api_list_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'body': p.body[:200] + '...' if len(p.body) > 200 else p.body,
        'author': p.author.username if p.author else None,
        'author_id': p.user_id,
        'created_at': p.created_at.isoformat() if p.created_at else None,
        'likes_count': p.likes.count() if hasattr(p, 'likes') else 0
    } for p in posts])


@api_v1_bp.route('/post/<int:id>', methods=['GET'])
def api_get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify({
        'id': post.id,
        'title': post.title,
        'body': post.body,
        'author': post.author.username if post.author else None,
        'author_id': post.user_id,
        'created_at': post.created_at.isoformat() if post.created_at else None,
        'likes_count': post.likes.count() if hasattr(post, 'likes') else 0
    })


@api_v1_bp.route('/post', methods=['POST'])
@token_required
def api_create_post():
    data = request.get_json() or {}

    if not data.get('title') or not data.get('body'):
        return jsonify({'error': 'Заголовок и текст обязательны'}), 400

    if len(data['body']) > 300:
        return jsonify({'error': 'Текст поста не может превышать 300 символов'}), 400

    post = Post(
        title=data['title'],
        body=data['body'],
        user_id=g.current_user.id
    )

    db.session.add(post)
    db.session.commit()

    return jsonify({'id': post.id, 'title': post.title}), 201


@api_v1_bp.route('/post/<int:id>', methods=['PUT'])
@token_required
def api_update_post(id):
    post = Post.query.get_or_404(id)

    if post.user_id != g.current_user.id and not g.current_user.is_admin():
        return jsonify({'error': 'Нет прав на редактирование'}), 403

    data = request.get_json() or {}

    if 'title' in data:
        post.title = data['title']
    if 'body' in data:
        if len(data['body']) > 300:
            return jsonify({'error': 'Текст поста не может превышать 300 символов'}), 400
        post.body = data['body']

    db.session.commit()

    return jsonify({'success': True, 'post': {
        'id': post.id,
        'title': post.title,
        'body': post.body
    }})


@api_v1_bp.route('/post/<int:id>', methods=['DELETE'])
@token_required
def api_delete_post(id):
    post = Post.query.get_or_404(id)

    if post.user_id != g.current_user.id and not g.current_user.is_admin():
        return jsonify({'error': 'Нет прав на удаление'}), 403

    if hasattr(post, 'likes'):
        Like.query.filter_by(post_id=id).delete()

    db.session.delete(post)
    db.session.commit()

    return jsonify({'success': True})


@api_v1_bp.route('/like/<int:post_id>', methods=['POST'])
@token_required
def api_like_post(post_id):
    post = Post.query.get_or_404(post_id)
    try:
        like = Like.query.filter_by(
            user_id=g.current_user.id,
            post_id=post_id
        ).first()

        if like:
            db.session.delete(like)
            db.session.commit()
            return jsonify({'likes': Like.query.filter_by(post_id=post_id).count()})
        else:
            like = Like(user_id=g.current_user.id, post_id=post_id)
            db.session.add(like)
            db.session.commit()
            return jsonify({'likes': Like.query.filter_by(post_id=post_id).count()})
    except: return jsonify({'likes': 0})