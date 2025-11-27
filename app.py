from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, reqparse, Resource, fields, marshal_with, abort, marshal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db=SQLAlchemy(app)
api = Api(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self, name, age):
        self.name = name
        self.age = age

def response_wrapper(success :bool, message :str , data=None):
    return {
        'success': success,
        'message': message,
        'data': data
    }


student_args = reqparse.RequestParser()
student_args.add_argument('name',type=str,location='json',required=True,help='Name cannot be blank')
student_args.add_argument('age',type=int,location='json',required=True,help='Age cannot be blank')

option_args = reqparse.RequestParser()
option_args.add_argument('age',type=int,location='json',required=True,help='Name cannot be blank')

studentFields = {
    'id':fields.Integer,
    'name':fields.String,
    'age':fields.Integer,
}

class Users(Resource):

    def get(self):
        users = Student.query.all()
        data=marshal(users,studentFields)
        return response_wrapper(True,"Success",data),200


    def post(self):
        args = student_args.parse_args()
        user = Student(name=args['name'],age=args['age'])
        db.session.add(user)
        db.session.commit()

        data=marshal(user,studentFields)
        return response_wrapper(True,"Student Created Successfully",data),201

class User(Resource):

    def get(self, id):
        user = Student.query.filter_by(id=id).first()
        if not(user):
            abort(404,message="Student does not exist")
        data=marshal(user,studentFields)
        return response_wrapper(True,"Success",data),200


    def put(self, id):
        args = option_args.parse_args()
        user = Student.query.filter_by(id=id).first()
        if not(user):
            abort(404,message="Student does not exist")
        user.age = args['age']
        db.session.commit()

        data=marshal(user,studentFields)
        return response_wrapper(True,"Success",data),200
        return user

api.add_resource(Users,'/student/')
api.add_resource(User,'/student/<int:id>/')
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
