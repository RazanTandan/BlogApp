from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from BlogApp import db, bcrypt
from BlogApp.models import User, Post
from BlogApp.users.forms import (RegistrationForm, LoginForm, AccountUpdateForm,
                                   ResetReqestForm, ResetPasswordForm)
from BlogApp.users.utils import save_picture, send_reset_email


users = Blueprint('users', __name__)



@users.route('/register', methods = ['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	register_form = RegistrationForm()
	if register_form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')  #Hashing the password 
		#Adding Data to Database
		user = User(username = register_form.username.data, email = register_form.email.data, password = hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('You have been successfully registered. Now you can log in.', 'success')
		return redirect(url_for('users.login'))
	return render_template('register.html', title = 'Register', form = register_form)


@users.route('/login', methods = ['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	login_form = LoginForm()
	if login_form.validate_on_submit():
		user = User.query.filter_by(email = login_form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, login_form.password.data):
			login_user(user, remember = login_form.remember.data)
			flash('You have been successfully login.', 'success')
			next_page =  request.args.get('next')
			print(next_page)
			return redirect(next_page) if next_page else redirect(url_for('main.index'))
		flash('Login Unsuccessful. Please check email and password.', 'danger')
	return render_template('login.html', title = 'Login', form = login_form)


@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.index'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	account_form = AccountUpdateForm()
	if account_form.validate_on_submit():
		if account_form.picture.data:
			picture_file = save_picture(account_form.picture.data)
			current_user.image_file = picture_file
		current_user.username = account_form.username.data
		current_user.email = account_form.email.data
		db.session.commit()
		flash('Changes have been added successfully.', 'success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		account_form.username.data = current_user.username
		account_form.email.data = current_user.email	
	img_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
	return render_template('account.html', title = 'Account', img_file = img_file, form = account_form)


@users.route('/user/<string:username>')
def user_posts(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username = username).first_or_404()
	posts_by_user = Post.query.filter_by(author = user).order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5)
	return render_template('user_posts.html', posts = posts_by_user, user = user) 


@users.route('/reset_password', methods = ['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	reset_request_form = ResetReqestForm() 
	if reset_request_form.validate_on_submit():
		user = User.query.filter_by(email = reset_request_form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password.', 'info')
		return redirect(url_for('users.login'))
	return render_template('reset_request.html', title = 'Reset Password', form = reset_request_form) 


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expire token', 'warning')
		return redirect(url_for('users.reset_request'))
	reset_password_form = ResetPasswordForm()
	if reset_password_form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(reset_password_form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash('Your password has been updated! You are now able to log in', 'success')
		return redirect(url_for('users.login'))
	return render_template('reset_token.html', title = 'Reset Password', form = reset_password_form)