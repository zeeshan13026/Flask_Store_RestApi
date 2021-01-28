from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from section6.code.db import db
from section6.code.resources.item import Item, ItemList
from section6.code.resources.user import UserRegister
from section6.code.security import authenticate, identity
from section6.code.resources.store import Store,StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)


@app.before_first_request
def create_table():
    db.create_all()

''' jwt creates an end point that /auth'''
jwt = JWT(app, authenticate, identity)  # /auth



api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList,'/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
