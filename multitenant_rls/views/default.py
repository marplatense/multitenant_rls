from cornice.resource import resource, view
from cornice.schemas import validate_colander_schema
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest
from pyramid.security import Allow, Authenticated, ALL_PERMISSIONS, DENY_ALL
from pyramid_sqlalchemy import Session

from ..models import Product, City, User, Price
from ..models.mymodel import ProductSchema, CitySchema, UserSchema, PriceSchema


class BaseResource(object):

    __acl__ = [(Allow, Authenticated, ALL_PERMISSIONS), DENY_ALL]

    def __init__(self, request):
        self.request = request

    @view(renderer='json')
    def collection_get(self):
        return {'data': Session.query(self.model).order_by(self.model.id).all()}

    @view(renderer='json')
    def get(self):
        result = Session.query(self.model).get(int(self.request.matchdict['id']))
        if result:
            return result
        else:
            raise HTTPNotFound()

    @view(renderer='json')
    def delete(self):
        result = Session.query(self.model).get(int(self.request.matchdict['id']))
        if result and not result.is_readonly:
            Session.delete(result)
            return result
        else:
            raise HTTPNotFound()

    @view(renderer='json')
    def collection_post(self):
        if self.model.is_readonly:
            raise HTTPBadRequest()
        validate_colander_schema(self._schema, self.request)
        obj = self.model(**self.request.json_body)
        Session.add(obj)
        return obj

    @view(renderer='json')
    def put(self):
        if self.model.is_readonly:
            raise HTTPBadRequest()
        validate_colander_schema(self._schema, self.request)
        result = Session.query(self.model).get(int(self.request.matchdict['id']))
        if result:
            for k, v in self.request.json_body.items():
                setattr(self, k, v)
            return result
        else:
            raise HTTPNotFound()


@resource(collection_path='/products', path='/products/{id}')
class ProductAPI(BaseResource):

    def __init__(self, request):
        super(ProductAPI, self).__init__(request)
        self.model = Product
        self._schema = ProductSchema


@resource(collection_path='/cities', path='/city/{id}')
class CityAPI(BaseResource):

    def __init__(self, request):
        super(CityAPI, self).__init__(request)
        self.model = City
        self._schema = CitySchema


@resource(collection_path='/users', path='/users/{id}')
class UsersAPI(BaseResource):

    def __init__(self, request):
        super(UsersAPI, self).__init__(request)
        self.model = User
        self._schema = UserSchema


@resource(collection_path='/prices', path='/prices/{id}')
class PriceAPI(BaseResource):

    def __init__(self, request):
        super(PriceAPI, self).__init__(request)
        self.model = Price
        self._schema = PriceSchema
