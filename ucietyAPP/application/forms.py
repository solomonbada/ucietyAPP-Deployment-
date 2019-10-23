from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, Form, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from application.models import University, StudentUsers, Society, Notes
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_login import LoginManager, current_user, UserMixin

######################STUDENT REGISTRATION FORM#############################

class StudentRegistrationForm(FlaskForm):
	first_name = StringField('First Name',
		validators=[
			DataRequired(),
			Length(min=2, max=15)
		])
	last_name = StringField('Last Name',
		validators=[
			DataRequired(),
			Length(min=2, max=15)
        ])

	lists = University.query.filter_by(uni_name=University.uni_name).all()
	names = []

	for i in range(int(len(lists))):
		temp = [lists[i].id, lists[i].uni_name]
		names.append(temp)

	uni_id = SelectField("University",
		choices=names,
		coerce=int) 

	lists = University.query.filter_by(uni_name=University.uni_name).all()
	names = []

	for i in range(int(len(lists))):
		temp = [lists[i].uni_name, lists[i].uni_name]
		names.append(temp)

	uni_name = SelectField("Confirm University",
		validators=[
			DataRequired()],
		choices=names) 

	email = StringField('Email',
		validators=[
			DataRequired(),
			Length(min=2, max=50),
			Email()
		])
	password = PasswordField('Password',
		validators=[
			DataRequired()
		])
	confirm_password = PasswordField('Confirm Password',
		validators=[
			DataRequired(),
			EqualTo('password', message='Your passwords do not match!')
		])
	submit = SubmitField('Sign Up')

	def validate_email(self, email):
		user=StudentUsers.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email already in use!')

	def validate_first_name(self, first_name):

		alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
		for character in first_name.data:
			if character not in alphabet:
				raise ValidationError('Please use only alphabet letters!')

	def validate_last_name(self, last_name):

		alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
		for character in last_name.data:
			if character not in alphabet:
				raise ValidationError('Please use only alphabet letters!')


##########################################################################
######################STUDENT LOGIN FORM####################################

class StudentLoginForm(FlaskForm):
	email = StringField('Email',
		validators=[
			DataRequired(),
			Email()
		])
	password = PasswordField('Password',
		validators=[
			DataRequired()
		])
	remember = BooleanField('Remember Me') 
	submit = SubmitField('Login')

##########################################################################
######################UPDATE ACCOUNT FORM####################################

class UpdateAccountForm(FlaskForm):
	first_name = StringField('First Name',
		validators=[
			DataRequired(),
			Length(min=2, max=15),
		])
	last_name = StringField('Last Name',
		validators=[
			DataRequired(),
			Length(min=2, max=15),
        ])

	email = StringField('Email',
		validators=[
			DataRequired(),
			Length(min=2, max=50),
			Email()
		])

	lists = Society.query.filter_by(uni_id=StudentUsers.uni_id).all() 
	names = []

	for i in range(int(len(lists))):
		temp = [lists[i].SocietyName, lists[i].SocietyName] 
		names.append(temp) 

	SocietyName = SelectField("Confirm University",
		choices=names)

	submit = SubmitField('Update')

	def validate_email(self, email): 
		if email.data != current_user.email:
			user=StudentUsers.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Email already in use! - Please choose another')

######################NOTES FORM###################################################

class NotesForm(FlaskForm):
	title = StringField('Title', 
		validators=[
			DataRequired(),
			Length(min=4, max=100),
		])
	content = TextAreaField('Content', 
		validators=[
			DataRequired(),
			Length(min=10, max=10000),
		])
	submit = SubmitField('Post Note')


