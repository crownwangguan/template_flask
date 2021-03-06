from flask_restplus import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from .model import Store as StoreModel
from .schema import StoreSchema


api = Namespace('stores', path='/', description='Operations related to stores')


store = api.model('Store', {
    'name': fields.String(description='Store Name', required=True),
})

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)


@api.doc(params={'name': 'Store name'})
class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store_schema.dump(store), 200
        return {'message': 'Store not found'}, 404

    @jwt_required()
    @api.expect(store)
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except Exception:
            return {"message": "An error occurred creating the store."}, 500

        return store_schema.dump(store), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):
    @classmethod
    def get(cls):
        return {"stores": store_list_schema.dump(StoreModel.find_all())}, 200


api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
