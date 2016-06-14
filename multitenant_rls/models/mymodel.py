import colander
from pyramid_sqlalchemy import Session
from sqlalchemy import (
    Table,
    Integer,
    String,
    Column,
    ForeignKey,
    Numeric
)
from sqlalchemy.orm import relationship


from .meta import Base


class JSONify(object):

    __ro = False

    @property
    def is_readonly(self):
        return self._ro

    def __json__(self, request):
        return dict([(k, v) for k, v in self.__dict__.items() if not k.startswith('_')])


class Product(Base, JSONify):
    """This class is here to demonstrate that some tables can be global and not restricted per client"""
    __tablename__ = "products"
    _ro = True
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class ProductSchema(colander.MappingSchema):
    id = colander.SchemaNode(colander.Integer(), location='body', type='int', missing=colander.drop)
    name = colander.SchemaNode(colander.String(), location='body', type='str')


class City(Base, JSONify):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class CitySchema(colander.MappingSchema):
    id = colander.SchemaNode(colander.Integer(), location='body', type='int', missing=colander.drop)
    name = colander.SchemaNode(colander.String(), location='body', type='str')


class User(Base, JSONify):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)

    @classmethod
    def login(cls, username, password):
        user = Session.query(cls).filter(cls.username == username).first()
        return user


class UserSchema(colander.MappingSchema):
    id = colander.SchemaNode(colander.Integer(), location='body', type='int', missing=colander.drop)
    username = colander.SchemaNode(colander.String(), location='body', type='str', validator=colander.Email)


city_users = Table('city_users', Base.metadata,
                   Column('user_id', Integer, ForeignKey('users.id'), unique=True, index=True),
                   Column('city_id', Integer, ForeignKey('cities.id'), nullable=False, index=True))


class Price(Base, JSONify):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, index=True)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False, index=True)
    value = Column(Numeric, nullable=False, default=0)

    product = relationship(Product)
    city = relationship(City)


class PriceSchema(colander.MappingSchema):
    id = colander.SchemaNode(colander.Integer(), location='body', type='int', missing=colander.drop)
    product_id = colander.SchemaNode(colander.Integer(), location='body', type='int')
    city_id = colander.SchemaNode(colander.Integer(), location='body', type='int')
    value = colander.SchemaNode(colander.Decimal(), location='body', type='int', missing=colander.Range(min=1))


City.users = relationship(User, secondary=city_users)
User.city = relationship(City, secondary=city_users, uselist=False)