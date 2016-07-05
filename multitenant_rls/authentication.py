from pyramid.security import Allow, Authenticated, ALL_PERMISSIONS, unauthenticated_userid
from pyramid_sqlalchemy import Session

from .models import User


def check(username, password, request):
    """
    Validates a given user exists in the system, in case it both ```my.username``` and ```my.city```
    are set as PG global variables and an ample principal for the Authenticated user is returned.
    If user does not exist, return None
    """
    user = User.login(username=username, password=password)
    if user is not None:
        return [(Allow, Authenticated, ALL_PERMISSIONS)]
    return user


def get_user(request):
    userid = unauthenticated_userid(request)
    if userid is not None:
        return Session.query(User).get(userid)

