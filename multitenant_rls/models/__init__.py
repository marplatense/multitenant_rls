from pyramid_sqlalchemy import Session
from sqlalchemy import engine_from_config, event, DDL
from sqlalchemy.orm import configure_mappers

# import or define all models here to ensure they are attached to the
# Base.metadata prior to any initialization routines
from .mymodel import Product, City, User, Price # flake8: noqa

# run configure_mappers after defining all of the models to ensure
# all relationships can be setup
configure_mappers()


def get_engine(settings, prefix='sqlalchemy.'):
    return engine_from_config(settings, prefix)


def includeme(config):
    """
    Initialize the model for a Pyramid app.

    Activate this setup using ``config.include('multitenant_rls.models')``.

    """
    settings = config.get_settings()
    engine = engine_from_config(settings)
    Session.configure(bind=engine)

    # use pyramid_tm to hook the transaction lifecycle to the request
    config.include('pyramid_tm')

enable_rls_str = "alter table %(table)s enable row level security"
"""Activate RLS for the given table"""

tenancy_policy_str = "create policy %(table)s_tenancy_policy on %(table)s for all " \
                     "using (city_id=current_setting('my.city_id')::integer) " \
                     "with check (city_id=current_setting('my.city_id')::integer)"
"""Create the city constraint policy for the given table"""

event.listen(Price.__table__, 'after_create', DDL(enable_rls_str))
event.listen(Price.__table__, 'after_create', DDL(tenancy_policy_str))
"""In case you want to apply the policy to more than one table, the keyword Table can be used instead naming each table
separately."""
