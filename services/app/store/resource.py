from flask_restplus import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from .model import Store as StoreModel


api = Namespace('stores', path='/', description='Operations related to stores')


store = api.model('Store', {
    'name': fields.String(description='Store Name', required=True),
})


@api.doc(params={'name': 'Store name'})
class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
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

        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': [x.json() for x in StoreModel.query.all()]}


api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')