from pyramid.security import Allow, Authenticated, ALL_PERMISSIONS
#from sqlalchemy import func, cast, String
#from sqlalchemy.orm import object_session
from .models import User


def check(username, password, request):
    """
    Validates a given user exists in the system, in case it both ```my.username``` and ```my.city```
    are set as PG global variables and an ample principal for the Authenticated user is returned.
    If user does not exist, return None
    """
    user = User.login(username=username, password=password)
    if user is not None:
        #res = object_session(user).query(func.set_config('my.city_id', str(user.city.id), True)).one()
        return [(Allow, Authenticated, ALL_PERMISSIONS)]
    return user
