from ..config import cfg
from ..db import *
from .. import util
import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, or_

from flask import abort
from datetime import date, time, timezone
import requests
import os
import nanoid


def get_report(e_id, r_id):
    with get_session() as s:
        event = s.query(Event).get(e_id)
        if not event or event.status == 'deleted':
            abort(404, 'No event with this id')

        report = s.query(Participation, User).filter(
                User.id == Participation.u_id,
                Participation.id == r_id,
                Participation.participation_role == 'presenter'
        ).one_or_none()

        if not report:
            abort(404, 'Report not found by this id')

        return {
            'email': report.User.email,
            'name': report.User.name,
            'surname': report.User.surname,
            "report": report.Participation.report,
            "presenter_description": report.Participation.presenter_description,
            "report_description": report.Participation.report_description,
            "report_status": report.Participation.report_status
        }
