from cornice.resource import resource, view
from cornice.schemas import validate_colander_schema
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest
from pyramid.security import Allow, Authenticated, ALL_PERMISSIONS, DENY_ALL
from pyramid_sqlalchemy import Session
from sqlalchemy import select, func, cast, String
import transaction

from ..models import Product, City, User, Price
from ..models.mymodel import ProductSchema, CitySchema, UserSchema, PriceSchema


def check_acl(request):
    return [(Allow, Authenticated, ALL_PERMISSIONS), DENY_ALL]


def set_config(user):
    stmt = select([func.set_config(cast('my.city_id', String), cast(user.city.id, String), True)])
    Session.execute(stmt)


class BaseResource(object):

    def __init__(self, request):
        self.request = request

    @view(renderer='json')
    def collection_get(self):
        set_config(self.request.user)
        return {'data': Session.query(self.model).order_by(self.model.id).all()}

    @view(renderer='json')
    def get(self):
        set_config(self.request.user)
        result = Session.query(self.model).get(int(self.request.matchdict['id']))
        if result:
            return result
        raise HTTPNotFound()

    @view(renderer='json')
    def delete(self):
        set_config(self.request.user)
        result = Session.query(self.model).get(int(self.request.matchdict['id']))
        if result and not result.is_readonly:
            Session.delete(result)
            return result
        raise HTTPNotFound()

    @view(renderer='json')
    def collection_post(self):
        set_config(self.request.user)
        if self.model.is_readonly:
            raise HTTPBadRequest()
        validate_colander_schema(self._schema, self.request)
        obj = self.model(**self.request.json_body)
        Session.add(obj)
        return obj

    @view(renderer='json')
    def put(self):
        set_config(self.request.user)
        if self.model.is_readonly:
            raise HTTPBadRequest()
        validate_colander_schema(self._schema, self.request)
        result = Session.query(self.model).get(int(self.request.matchdict['id']))
        if result:
            for k, v in self.request.json_body.items():
                setattr(result, k, v)
            return result
        raise HTTPNotFound()


@resource(collection_path='/products', path='/products/{id}', acl=check_acl)
class ProductAPI(BaseResource):

    def __init__(self, request):
        super(ProductAPI, self).__init__(request)
        self.model = Product
        self._schema = ProductSchema


@resource(collection_path='/cities', path='/city/{id}', acl=check_acl)
class CityAPI(BaseResource):

    def __init__(self, request):
        super(CityAPI, self).__init__(request)
        self.model = City
        self._schema = CitySchema


@resource(collection_path='/users', path='/users/{id}', acl=check_acl)
class UsersAPI(BaseResource):

    def __init__(self, request):
        super(UsersAPI, self).__init__(request)
        self.model = User
        self._schema = UserSchema


@resource(collection_path='/prices', path='/prices/{id}', acl=check_acl)
class PriceAPI(BaseResource):

    def __init__(self, request):
        super(PriceAPI, self).__init__(request)
        self.model = Price
        self._schema = PriceSchema
