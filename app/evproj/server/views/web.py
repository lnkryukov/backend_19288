from flask import (Blueprint, request, redirect, url_for,
                   render_template, jsonify, abort)
from flask_login import (login_required, login_user, logout_user,
                         login_fresh, current_user)
from passlib.hash import sha256_crypt
from .. import auth
from .. import forms
from .. import api
import logging


mod = Blueprint('general', __name__)


@mod.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('general.home'))
    form = forms.AuthForm(request.form)
    message = ''
    if request.method == "POST" and form.validate_on_submit():
        user = auth.check_user(form.login.data)
        if user:
            if sha256_crypt.verify(form.password.data, user.password):
                login_user(user)
                return redirect(url_for('general.home'))
            else:
                message = 'Invalid password'
        else:
            message = 'Invalid user'
    return render_template('login.html', form=form, message=message)


@mod.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('general.home'))
    form = forms.RegisterForm(request.form)
    message = ''
    if request.method == "POST" and form.validate_on_submit():
        try:
            api.register_user(form.login.data,
                                form.mail.data,
                                form.name.data,
                                form.surname.data,
                                sha256_crypt.encrypt(str(form.password.data)))
            message = f'{form.login.data} was registered'
            form.login.data = ''
            form.mail.data = ''
            form.name.data = ''
            form.surname.data = ''
            form.password.data = ''
            form.password_repeat.data = ''
        except Exception as e:
            message = 'Failed to register user, probably one already exists.\n{}'.format(str(e))
    return render_template('register.html', form=form, message=message)


@mod.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('general.home'))


@mod.route('/')
@mod.route('/home')
def home():
    events = api.get_events()
    return render_template(
        'home.html',
        events=events,
    )


@mod.route('/cabinet')
@login_required
def cabinet():
    return render_template(
        '/cabinet.html',
        user=current_user,
    )


@mod.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = forms.CreateEvent(request.form)
    message = ''
    if request.method == "POST" and form.validate_on_submit():
        try:
            print('creating')
            api.create_event(form.name.data, current_user.login, form.date_time.data)
            message = f'{form.name.data} was created'
            form.name.data = ''
            form.date_time.data = ''
        except Exception as e:
            message = 'Failed to create event.\n{}'.format(str(e))
    return render_template(
        '/create_event.html',
        form=form,
        message=message,
    )


@mod.route('/event/<string:id>')
def eventе(id):
    event = api.get_event_info(id)
    print(event)
    return render_template(
        '/event.html',
        event=event,
    )


@mod.route('/confirmation/<string:name>')
def event(name):
    if current_user.is_authenticated:
        pass
    else:
        return render_template(
            'event.html',
            name=name,
        )


@mod.route('/blank')
def blank():
    return render_template('blank.html')


def page_not_found(e):
    if current_user.is_authenticated:
        return render_template(
            '404.html',
            login=current_user.login
        ), 404
    else:
        return render_template(
            '404.html',
            login=''
        ), 404
