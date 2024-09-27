from flask import Blueprint, url_for, flash, redirect, render_template, abort, request
from flask_login import current_user, login_required
from blogmon import db
from blogmon.models import Post
from blogmon.posts.forms import PostForm

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods = ['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has has been created!', 'success')
        return redirect(url_for('main.feed'))
    return render_template('create_post.html', title='New Post', form=form)

@posts.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    form.title.data = post.title
    form.content.data = post.content
    
    if form.validate_on_submit():
        post.title = form.title.data  # Update the title
        post.content = request.form.get('content')  # Update the content from the hidden input
        db.session.commit()  # Commit the changes to the database
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.post', post_id=post.id))
    return render_template('update_post.html', title='Update Post', post=post, form=form)

@posts.route("/post/<int:post_id>/delete", methods = ['GET','POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    previous_page = request.args.get('previous')
    return redirect(previous_page) if previous_page else redirect(url_for('main.feed'))
