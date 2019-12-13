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
        user = auth.check_user(form.mail.data)
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
            api.register_user(form.mail.data,
                                form.name.data,
                                form.surname.data,
                                sha256_crypt.encrypt(str(form.password.data)))
            message = f'{form.login.data} was registered'
            form.mail.data = ''
            form.name.data = ''
            form.surname.data = ''
            form.password.data = ''
            form.password_repeat.data = ''
        except Exception as e:
            message = 'Failed to register user, probably one already exists.\n{}'.format(str(e))
        return redirect(url_for('general.login'))
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
            last_id = api.create_event(form.name.data,
                                        form.sm_description.data,
                                        form.description.data,
                                        form.date_time.data,
                                        form.phone.data,
                                        form.mail.data)
            api.create_event_creator(current_user.id, last_id)
            message = f'{form.name.data} was created'
            form.name.data = ''
            form.sm_description.data = ''
            form.description.data = ''
            form.date_time.data = ''
            form.phone.data = ''
            form.mail.data = ''
        except Exception as e:
            message = 'Failed to create event.\n{}'.format(str(e))
        return redirect(url_for('general.home'))
    return render_template(
        '/create_event.html',
        form=form,
        message=message,
    )


@mod.route('/event/<string:id>')
def event(id):
    if api.event_exist(id):
        event = api.get_event_info(id)
        users = api.get_participators(id)
        if current_user.is_authenticated:
            entering = api.check_participation(current_user.id, id)
            if (entering == 'monitoring'):
                conf, unconf = api.get_stat(id)
                return render_template(
                    '/event_page.html',
                    event=event,
                    users=users,
                    entering=entering,
                    conf=conf,
                    unconf=unconf,
                )
            return render_template(
                '/event_page.html',
                event=event,
                users=users,
                entering=entering,
            )
        else:
            return render_template(
                '/event_page.html',
                event=event,
                users=users,
                entering='not joined',
            )
    else:
        abort(404)


@mod.route('/join/<string:id>', methods=['GET', 'POST'])
@login_required
def join(id):
    if api.event_exist(id):
        api.guest_join(current_user.id, id)
        return redirect(url_for('general.event', id=id))
    else:
        abort(404)


def page_not_found(e):
    if current_user.is_authenticated:
        return render_template(
            '404.html',
            login=current_user.mail
        ), 404
    else:
        return render_template(
            '404.html',
            login=''
        ), 404
