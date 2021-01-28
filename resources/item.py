from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
import sqlite3

from section6.code.models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field can't be left blank"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id."
                        )

    @jwt_required()
    def get(self, name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items WHERE name = ?"
        # result = cursor.execute(query,(name,))
        # row = result.fetchone()
        #
        # if row:
        #     return {'item':{'name':row[0], 'price' : row[1]}}, 200

        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'item not found'},404
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # # for item in items:
        # #     if item['name'] == name:
        # #         return item
        # return {'item': item}, 200 if item is not None else 404

    def post(self, name):
        # if next(filter(lambda x: x['name'] == name, items), None):
        #     return {'message': 'An item with name {} already exist'.format(name)}, 400
        if ItemModel.find_by_name(name):
            return {"message":"An item with name '{}' already exist".format(name)},400
        data = Item.parser.parse_args()
#        data = request.get_json()  # Getting data from the post request

        item = ItemModel(name, data['price'],data['store_id'])
        # item = ItemModel(name, **data)

        # items.append(item)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occured"},500 # Internal server error

        return item.json(), 201

    def delete(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'item deleted'}

        # # global items
        # # items = list(filter(lambda x: x['name'] != name, items))
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = 'DELETE FROM items WHERE name = ?'
        # cursor.execute(query, (name,))
        #
        # connection.commit()
        # connection.close()
        # return {'message': 'item deleted'}

    def put(self, name):

        #data = request.get_json()
        data = Item.parser.parse_args()
        #item = next(filter(lambda x: x['name'] == name, items), None)
        item = ItemModel.find_by_name(name)
        # update_item = ItemModel(name,data['price'])

        if item is None:
            item = ItemModel(name,data['price'],data['store_id'])
            # try:
            #     update_item.insert()
            # except:
            #     return {'message':'An error occured inserting the item'},500
        else:
            item.price = data['price']
            item.store_id = data['store_id']
            # try:
            #     update_item.update()
            # except:
            #     return {'message':'An error occured updating the item'},500
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items' : [item.json() for item in ItemModel.query.all()]}
        # return {'items' : list(map(lambda x:x.json(), ItemModel.query.all()))}


        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = 'SELECT * FROM items'
        # result = cursor.execute(query)
        #
        # items = []
        # for row in result:
        #     items.append({'name':row[0],'price':row[1]})
        #
        # connection.close()
        # return {'items': items}