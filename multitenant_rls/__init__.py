from pyramid.authentication import BasicAuthAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.decorator import reify
from pyramid.request import Request
from pyramid.security import unauthenticated_userid, Authenticated


from .authentication import check


class RequestWithUserAttribute(Request):
    @reify
    def user(self):
        userid = unauthenticated_userid(self)
        if userid is not None:
            pass


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_sqlalchemy')
    config.include('cornice')
    config.include('.models')
    config.include('.routes')
    config.set_authentication_policy(BasicAuthAuthenticationPolicy(check=check))
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.set_default_permission(Authenticated)
    config.set_request_factory(RequestWithUserAttribute)
    config.scan()
    return config.make_wsgi_app()
