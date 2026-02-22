from flask import Blueprint, render_template, g, redirect
from app.models.post import Post

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)

@main_bp.route('/create')
def create_post_form():
    return render_template('create_post.html')

@main_bp.route('/edit/<int:id>')
def edit_post_form(id):
    post = Post.query.get_or_404(id)
    return render_template('edit_post.html', post=post)

@main_bp.route('/logout')
def logout():
    return '''
    <script>
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/';
    </script>
    '''