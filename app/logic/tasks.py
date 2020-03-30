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


def create_task(e_id, data):
    deadline = None
    if 'deadline' in data.keys():
        ddate = data['deadline'].split('-')
        deadline = date(int(ddate[0]), int(ddate[1]), int(ddate[2]))
    with get_session() as s:
        event = s.query(Event).get(e_id)
        if not event or event.status == 'deleted':
            abort(404, 'No event with this id')

        task = ETask(e_id=e_id, name=data['name'],
                      description=data['description'], deadline=deadline)
        s.add(task)


def delete_task(e_id, t_id):
    with get_session() as s:
        event = s.query(Event).get(e_id)
        if not event or event.status == 'deleted':
            abort(404, 'No event with this id')

        task = s.query(ETask).filter(
                ETask.id == t_id,
                ETask.e_id == e_id
        ).one_or_none()

        if not task or task.status == 'deleted':
            abort(404, 'No task with this id')

        task.status = 'deleted'


def move_task(e_id, t_id, status):
    with get_session() as s:
        event = s.query(Event).get(e_id)
        if not event or event.status == 'deleted':
            abort(404, 'No event with this id')

        task = s.query(ETask).filter(
                ETask.id == t_id,
                ETask.e_id == e_id
        ).one_or_none()

        if not task or task.status == 'deleted':
            abort(404, 'No task with this id')
        if task.status == status:
            abort(409, 'Task already have this status')

        task.status = status


def get_tasks(e_id):
    result = []
    with get_session() as s:
        event = s.query(Event).get(e_id)
        if not event or event.status == 'deleted':
            abort(404, 'No event with this id')

        tasks = s.query(ETask).filter(
                ETask.status != 'deleted',
                ETask.e_id == e_id
        ).all()

        for task in tasks:
            deadline = None
            if task.deadline is not None:
                deadline = task.deadline.isoformat()

            result.append({
                'id': task.id,
                'name': task.name,
                'description': task.description,
                'deadline': deadline,
                'status': task.status
            })
    return result


def update_task(e_id, t_id, data):
    with get_session() as s:
        event = s.query(Event).get(e_id)
        if not event or event.status == 'deleted':
            abort(404, 'No event with this id')

        task = s.query(ETask).filter(
                ETask.id == t_id,
                ETask.e_id == e_id
        ).one_or_none()

        if not task or task.status == 'deleted':
            abort(404, 'No task with this id')

        for arg in data.keys():
            getattr(event, arg)
            if arg in ['id', 'status', 'e_id']:
                abort(400, "Can't change this field(s)")
            if arg == 'deadline':
                ddate = data['deadline'].split('-')
                deadline = date(int(ddate[0]), int(ddate[1]), int(ddate[2]))
                setattr(task, arg, deadline)
            else:
                setattr(task, arg, data[arg])
