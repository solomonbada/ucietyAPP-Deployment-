from flask import render_template, url_for, redirect, request
from application import app, db, bcrypt
from application.models import StudentUsers, Society, University, Notes
from application.forms import StudentRegistrationForm, StudentLoginForm, UpdateAccountForm, NotesForm
from flask_login import login_user, current_user, logout_user, login_required
from wtforms_sqlalchemy.fields import QuerySelectField
import sqlite3

@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register(): 
	if current_user.is_authenticated:
		return redirect(url_for('mytimeline'))	
	form = StudentRegistrationForm()
	if form.validate_on_submit(): 
		hashed_password = bcrypt.generate_password_hash(form.password.data) 
		user = StudentUsers(first_name=form.first_name.data.capitalize(), last_name=form.last_name.data.capitalize(), uni_id=form.uni_id.data, uni_name=form.uni_name.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit() 
		return redirect(url_for('login')) 
	return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('mytimeline'))
	else:
		form = StudentLoginForm()
		if form.validate_on_submit():
			user = StudentUsers.query.filter_by(email=form.email.data).first() 
			if user and bcrypt.check_password_hash(user.password, form.password.data):
				login_user(user, remember=form.remember.data)
				return redirect(url_for('mytimeline'))
		return render_template('login.html', title='Login', form=form)


@app.route('/mytimeline', methods=['GET', 'POST'])
@login_required 
def mytimeline():
	form = NotesForm
	if current_user.is_authenticated: 
		notes = Notes.query.filter_by(mine=current_user).all()
		return render_template('mytimeline.html', title='My Timeline', notes=notes, mine=current_user, form=form)
	return render_template('mytimeline.html', title='My Timeline', notes=notes, mine=current_user, form=form)
 

@app.route('/account', methods=['GET', 'POST'])
@login_required 
def account():
	form = UpdateAccountForm() 
	if form.validate_on_submit():
		current_user.first_name = form.first_name.data.capitalize()
		current_user.last_name = form.last_name.data.capitalize()
		current_user.email = form.email.data
		current_user.soc_name = form.SocietyName.data
		db.session.commit() 
		return redirect(url_for('account'))
	elif request.method == 'GET': 
		form.first_name.data = current_user.first_name
		form.last_name.data = current_user.last_name
		form.email.data = current_user.email
		lists = Society.query.filter_by(uni_id=current_user.uni_id).all() 
		names = []
		for i in range(int(len(lists))):
			temp = [lists[i].SocietyName, lists[i].SocietyName] 
			names.append(temp)
		form.SocietyName.choices=names
	return render_template('account.html', title='Account', form=form, creator=current_user)


@app.route('/viewsocieties')
@login_required 
def viewsocieties():
	if current_user.is_authenticated: 
		societies = Society.query.filter_by(uni_id=current_user.uni_id)
	return render_template('viewsocieties.html', title='View Societies', societies=societies, creator=current_user)


@app.route('/viewsocieties/<int(min=1):society_id>')
@login_required
def more(society_id):
	society1 = Society.query.filter_by(id=society_id).first() 
	return render_template('more.html', title='More Info', society=society1)


@app.route('/notes', methods=['GET', 'POST'])
@login_required
def note():
	form = NotesForm() 
	if form.validate_on_submit():
		postData = Notes(
			title=form.title.data,
			content=form.content.data,
			mine=current_user
			)
		db.session.add(postData)
		db.session.commit() 
		return redirect(url_for('mytimeline')) 
	else:
		print(form.errors)
	return render_template('notes.html', title='Create Note', form=form)


@app.route("/notes/<int(min=1):note_id>/delete", methods=['POST'])
@login_required
def delete_post(note_id):
	note = Notes.query.filter_by(id=note_id).first() 
	db.session.delete(note) 
	db.session.commit() 
	return redirect(url_for('mytimeline'))

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))