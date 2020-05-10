from data import db_session
from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from parser import parser_job
from data.news import *


class UsersResource(Resource):
    def get(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        return jsonify({'news': jobs.to_dict(
            only=('team_leader', 'job', 'id', 'collaborators', 'is_finished'))})

    def delete(self, job_id):
        abort_if_jobs_not_found(job_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(job_id)
        session.delete(jobs)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'news': [item.to_dict(
            only=('team_leader', 'job', 'id', 'collaborators', 'is_finished')) for item in jobs]})

    def post(self):
        args = parser_job.parse_args()
        session = db_session.create_session()
        jobs = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            id=args['id'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished']
        )
        session.add(jobs)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_jobs_not_found(job_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(job_id)
    if not jobs:
        abort(404, message=f"Users {job_id} not found")
