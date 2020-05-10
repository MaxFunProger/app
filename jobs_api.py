import flask
from flask import jsonify
from data import db_session
from flask import request, abort
from data.users import *
from data.news import *
from data.departments import *
from flask import render_template
from data.register import RegisterForm
from data.login import LoginForm
from data.add_job import JobForm
from data.add_dep import DepForm
from flask import redirect
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

blueprint = flask.Blueprint('jobs_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify(
        {
            'news':
                [item.to_dict(only=('id', 'team_leader', 'job', 'work_size',
                                    'collaborators', 'start_date', 'end_date', 'is_finished', 'user_id'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(job_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    else:
        return jsonify(
            {
                'jobs':
                    jobs.to_dict(only=('id', 'team_leader', 'job', 'work_size',
                                       'collaborators', 'start_date', 'end_date', 'is_finished', 'user_id'))
            }
        )


@blueprint.route('/api/jobs', methods=['POST'])
def add_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'work_size', 'collaborators',
                  'start_date', 'end_date', 'is_finished', 'user_id']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    if session.query(Jobs).filter(Jobs.id == request.json['id']).first():
        return jsonify({'error': 'Id already exists'})
    jobs = Jobs(
        id=request.json['id'],
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        start_date=request.json['start_date'],
        end_date=request.json['end_date'],
        is_finished=request.json['is_finished'],
        user_id=request.json['user_id']
    )
    session.add(jobs)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def del_job(job_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(job_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    session.delete(jobs)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def edit_job(job_id):
    if not request.json():
        return jsonify({'error': 'Not found'})
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'work_size', 'collaborators',
                  'start_date', 'end_date', 'is_finished', 'user_id']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    jobs = session.query(Jobs).get(job_id)
    jobs.team_leader = request.json['team_leader']
    jobs.job = request.json['job']
    jobs.work_size = request.json['work_size']
    jobs.collaborators = request.json['collaborators']
    jobs.start_date = request.json['start_date']
    jobs.end_date = request.json['end_date']
    jobs.is_finished = request.json['is_finished']
    session.commit()
    return jsonify({'success': 'OK'})
