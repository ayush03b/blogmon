from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user
from blogmon.models import Post

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.feed'))
    return render_template('home.html', title='Home')
@main.route("/feed")
def feed():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=15)
    return render_template('feed.html', posts=posts, title='Feed')
