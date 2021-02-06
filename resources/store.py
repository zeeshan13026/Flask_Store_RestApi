from flask_restful import Resource,reqparse
from models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="Store name field can't be left blank"
                        )


    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message':'Store not found'},400

    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message':'A store with name {} is already exist'.format(name)}
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message':'An error occured while creating a store'},500

        return store.json(),201

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'Store deleted'}


class StoreList(Resource):
    def get(self):
        return {'store': [store.json() for store in StoreModel.query.all()]}