import os
from flask import Blueprint, redirect, url_for, flash, render_template, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from blogmon import db, bcrypt
from blogmon.models import User, Post
from blogmon.users.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm, UpdateProfileForm
from blogmon.users.utils import send_reset_email, save_picture

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.feed'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        # Log the user in after registration
        login_user(new_user)
        flash(f'Account created for {form.username.data} ^_^ !', 'success')
        return redirect(url_for('main.feed'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', 'danger')
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.feed'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.feed'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.feed'))

@users.route("/user/<string:username>")
@login_required
def user_profile(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=10)
    image_file = url_for('static', filename='profile_imgs/' + user.image_file)
    return render_template('user_profile.html', posts=posts, user=user, title=user.username, image_file=image_file)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('users.feed'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('users.feed'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@users.route("/profile", methods=['GET','POST'])
def profile():
    page = request.args.get('page', 1, type=int)
    user = current_user
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=10)
    form = UpdateProfileForm()
    
    if form.validate_on_submit():
        # Check for changes
        if (form.username.data != current_user.username) or (form.email.data != current_user.email):
            current_user.username = form.username.data
            current_user.email = form.email.data

        # Handle the file upload
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and file.filename != '':
                # Check if there is an existing profile image
                old_image_file = current_user.image_file
                if old_image_file and old_image_file != 'default.jpg':
                    # Delete the old image file
                    old_file_path = os.path.join(current_app.root_path, 'static/profile_imgs', old_image_file)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)

                # Use the save_picture function from utils
                picture_fn = save_picture(file)  # Call your save_picture function
                current_user.image_file = picture_fn  # Update the user's profile picture

        db.session.commit()
        flash('Account updated!', 'success')
        return redirect(url_for('users.profile'))
    
    image_file = url_for('static', filename='profile_imgs/' + current_user.image_file)
    return render_template('profile.html', title='Profile', image_file=image_file, form=form, posts=posts)
