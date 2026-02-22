from flask import Blueprint

blog_bp = Blueprint('blog', __name__, url_prefix='/posts')

from . import routes