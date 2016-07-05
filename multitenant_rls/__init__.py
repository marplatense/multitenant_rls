from pyramid.authentication import BasicAuthAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.security import Authenticated


from .authentication import check, get_user


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_sqlalchemy')
    config.include('cornice')
    config.set_authentication_policy(BasicAuthAuthenticationPolicy(check=check))
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.set_default_permission(Authenticated)
    config.add_request_method(get_user, 'user', reify=True)
    config.include('.models')
    config.scan()
    return config.make_wsgi_app()
