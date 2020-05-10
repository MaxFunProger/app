from data import db_session
from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from data.users import *
from parser import parser


class UsersResource(Resource):
    def get(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(User).get(news_id)
        return jsonify({'news': news.to_dict(
            only=('surname', 'name', 'user_id', 'position', 'speciality'))})

    def delete(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        users = session.query(User).get(user_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'news': [item.to_dict(
            only=('surname', 'name', 'user_id', 'position', 'speciality')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = User(
            surname=args['surname'],
            name=args['name'],
            user_id=args['user_id'],
            position=args['position'],
            speciality=args['speciality'],
            hashed_password=args['hashed_password']
        )
        session.add(users)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_news_not_found(user_id):
    session = db_session.create_session()
    news = session.query(User).get(user_id)
    if not news:
        abort(404, message=f"Users {user_id} not found")
