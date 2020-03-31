from flask import Blueprint, jsonify, request, abort, send_from_directory
from flask_login import (login_required, login_user, logout_user,
                         login_fresh, current_user)

import bcrypt

from . import *
from ..logic import events as events_logic
from ..logic.file_storage import file_storage_exceptions

bp = Blueprint('events', __name__, url_prefix='/event')


@bp.route('/<int:e_id>', methods=['GET'])
def event_by_id(e_id):
    if current_user.is_authenticated:
        return jsonify(part=events_logic.check_participation(current_user.id, e_id),
                       event=events_logic.get_event_info(e_id))
    else:
        return jsonify(part='not joined',
                       event=events_logic.get_event_info(e_id))


@bp.route('/<int:e_id>', methods=['PUT'])
@login_required
def put_event_by_id(e_id):
    if (current_user.service_status is 'user' and
        events_logic.check_participation(current_user.id, e_id) not in ['creator', 'manager']):
        return make_4xx(403, "No rights")
    data = get_json()
    events_logic.update_event(e_id, data)
    return make_ok(200, 'Successfully updated')


@bp.route('/<int:e_id>/delete', methods=['GET'])
@login_required
def delete_event_by_id(e_id):
    if (current_user.service_status is 'user' and
        events_logic.check_participation(current_user.id, e_id) is not 'creator'):
        return make_4xx(403, "No rights")
    events_logic.delete_event(e_id)
    return make_ok(200, 'Successfully deleted')


@bp.route('/', methods=['POST'])
@login_required
def create_event():
    data = get_json()
    last_id = events_logic.create_event(current_user.id, data)
    return make_ok(201, str(last_id))


@bp.route('/<int:e_id>/manager', methods=['POST'])
@login_required
def add_manager_to_event(e_id):
    data = get_json()
    if events_logic.check_participation(current_user.id, e_id) is not 'creator':
        return make_4xx(403, "No rights")
    action = events_logic.add_manager(e_id, data)
    return make_ok(200, 'Successfully ' + action + ' manager')


@bp.route('/<int:e_id>/manager/delete', methods=['GET'])
@login_required
def delete_manager_from_event(e_id):
    if events_logic.check_participation(current_user.id, e_id) is not 'creator':
        return make_4xx(403, "No rights")
    action = events_logic.delete_manager(e_id)
    return make_ok(200, 'Successfully delete manager')


@bp.route('/all', methods=['GET'])
def events():
    offset = request.args.get("offset", "")
    size = request.args.get("size", "")
    return jsonify(events_logic.get_events(offset, size))


@bp.route('/<int:e_id>/join', methods=['POST'])
@login_required
def join(e_id):
    data = get_json()
    events_logic.join_event(current_user.id, e_id, data)
    return make_ok(200, 'Successfully joined')

@bp.route('/<int:e_id>/report', methods=['POST'])
@login_required
def upload_report(e_id):
    
    if 'file' not in request.files:
        return make_4xx(403, "No file found")
    file = request.files['file']
    if file.filename == '':
        return make_4xx(403, "No file found")
    
    logging.info('Recieved file with content-length set as {}'.format(file.content_length))
    
    try:
        report_id = events_logic.upload_report(current_user.id, e_id, file)
    except file_storage_exceptions.FileSizeLimitError as e:
        return make_4xx(413, e.message)
    except (file_storage_exceptions.FileExtensionError, file_storage_exceptions.FileMimeTypeError) as e:
        return make_4xx(415, e.message)

    return make_ok(200, report_id)

@bp.route('/reports', methods=['GET'])
@login_required
def get_all_reports():
    if current_user.service_status is 'user':
        return make_4xx(403, "No rights")
    return jsonify(events_logic.get_all_reports())

@bp.route('/<int:e_id>/report', methods=['GET'])
def get_report(e_id):
    path, filename = events_logic.get_report(current_user.id, e_id)
    return send_from_directory(path, filename)

@bp.route('/<int:e_id>/report/info', methods=['GET'])
def get_report_info(e_id):
    return jsonify(events_logic.get_report_info(current_user.id, e_id))

@bp.route('/<int:e_id>/reports', methods=['GET'])
def get_reports(e_id):
    if current_user.service_status is 'user':
        return jsonify(events_logic.get_reports_for_event(e_id))
    else:
        return jsonify(events_logic.get_report_for_event_admin(e_id))

@bp.route('/<int:e_id>/report', methods=['DELETE'])
@login_required
def remove_report(e_id):
    events_logic.remove_report(current_user.id, e_id)
    return make_ok(200, 'Report removed successfully')

@bp.route('/<int:e_id>/presenters', methods=['GET'])
def presenters(e_id):
    return jsonify(events_logic.get_presenters(e_id))
