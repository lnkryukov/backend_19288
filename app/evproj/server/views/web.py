from flask import (Blueprint, request, redirect, url_for,
                   render_template, jsonify, abort)
from flask_login import (login_required, login_user, logout_user,
                         login_fresh, current_user)
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
        user = auth.dummy_auth(form.login.data, form.password.data)
        if user:
            login_user(user)
            return redirect(url_for('general.home'))
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
                                form.password.data)
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
    return redirect(url_for('general.login'))


@mod.route('/')
@mod.route('/home')
def home():
    if current_user.is_authenticated:
        pass
    else:
        return render_template(
            'home.html'
        )


@mod.route('/event/<string:name>')
def eventе(name):
    if current_user.is_authenticated:
        pass
    else:
        return render_template(
            '/event.html',
            name=name,
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
