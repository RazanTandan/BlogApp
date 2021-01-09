from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from BlogApp.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min = 2, max = 20)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
    	user = User.query.filter_by(username = username.data).first()
    	if user:
    		raise ValidationError('The username is already taken. Please choose a different one.')

    def validate_email(self, email):
    	email = User.query.filter_by(email = email.data).first()
    	if email:
    		raise ValidationError('The email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class AccountUpdateForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min = 2, max = 20)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    picture = FileField('Update Profile Picture', [FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update now')

    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username = username.data).first()
            if user: 
                raise ValidationError('The username is already taken. Please choose a different one.')
    
    def validate_email(self, email):
        if current_user.email != email.data:            
            email = User.query.filter_by(email = email.data).first()
            if email: 
                raise ValidationError('The email is already taken. Please choose a different one.')



class ResetReqestForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')