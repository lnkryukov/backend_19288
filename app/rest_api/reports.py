from flask import Blueprint, jsonify, request, make_response
from flask_login import (login_required, login_user, logout_user,
                         login_fresh, current_user)

import bcrypt

from . import *
from ..logic import reports as reports_logic, events as events_logic


bp = Blueprint('tasks', __name__, url_prefix='/event')


@bp.route('/<int:e_id>/report/<int:r_id>', methods=['GET'])
@login_required
def create_task(e_id, r_id):
    if events_logic.check_participation(current_user.id, e_id) is not 'manager':
        return make_4xx(403, "No rights")
    return jsonify(reports_logic.get_report(e_id, r_id))
