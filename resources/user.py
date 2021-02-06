import sqlite3
from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field can't be blank")

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field can't be blank")

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username is already exist"}, 400

        user = UserModel(data['username'],data['password'])
        # user = UserModel(**data)
        user.save_to_db()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "INSERT INTO users VALUES (NULL,?,?)"
        # cursor.execute(query,(data['username'],data['password']))
        #
        # connection.commit()
        # connection.close()

        return {"message": "user created successfully"}, 201
