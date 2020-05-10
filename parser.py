from flask_restful import reqparse


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('hashed_password', required=True)
parser.add_argument('user_id', required=True, type=int)

parser_job = reqparse.RequestParser()
parser_job.add_argument('id', required=True)
parser_job.add_argument('team_leader', required=True)
parser_job.add_argument('job', required=True, type=int)
parser_job.add_argument('work_size', required=True)
parser_job.add_argument('collaborators', required=True)
parser_job.add_argument('start_date', required=True)
parser_job.add_argument('end_date', required=True)
parser_job.add_argument('is_finished', required=True)

