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
from datetime import datetime

blueprint = flask.Blueprint('user_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/users', methods=['GET'])
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'age',
                                    'position', 'speciality', 'address', 'email', 'modified_date'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    session = db_session.create_session()
    users = session.query(Jobs).get(user_id)
    if not users:
        return jsonify({'error': 'Not found'})
    else:
        return jsonify(
            {
                'users':
                    users.to_dict(only=('id', 'surname', 'name', 'age',
                                       'position', 'speciality', 'address', 'email', 'modified_date'))
            }
        )


@blueprint.route('/api/users', methods=['POST'])
def add_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age', 'position',
                  'speciality', 'address', 'email', 'modified_date']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    if session.query(User).filter(User.id == request.json['id']).first():
        return jsonify({'error': 'Id already exists'})
    users = User(
        id=request.json['id'],
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        modified_date=request.json['modified_date']
    )
    session.add(users)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position',
                  'speciality', 'address', 'email']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        return jsonify({'error': 'Not found'})
    users.age = request.json['age']
    users.position = request.json['position']
    users.speciality = request.json['speciality']
    users.address = request.json['address']
    users.email = request.json['email']
    users.modified_date = datetime.now()
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def del_user(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        return jsonify({'error': 'Not found'})
    session.delete(users)
    session.commit()
    return jsonify({'success': 'OK'})
