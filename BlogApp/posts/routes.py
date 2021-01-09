
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from BlogApp import db
from BlogApp.models import Post
from BlogApp.posts.forms import PostForm

posts = Blueprint('posts', __name__)



@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
	post_form = PostForm()
	if post_form.validate_on_submit():
		new_post = Post(title = post_form.title.data, content = post_form.content.data, author = current_user)
		db.session.add(new_post)
		db.session.commit()
		flash('Your Post is successfully created.', 'success')
		return redirect(url_for('main.index'))
	return render_template('create_post.html', title='New Post', form = post_form, legend = 'New Post')


@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):	
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title = post.title, post = post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	post_form = PostForm()
	if post_form.validate_on_submit():
		post.title = post_form.title.data
		post.content = post_form.content.data
		db.session.commit()
		flash('Your post has been update!', 'success')
		return redirect(url_for('posts.post', post_id = post.id))
	elif request.method == 'GET':
		post_form.title.data = post.title
		post_form.content.data = post.content
	return render_template('create_post.html', title = post.title, form = post_form, legend = 'Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get(post_id)
	if post.author != current_user:		
		adort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Post has been deleted!', 'success')
	return redirect(url_for('main.index'))


