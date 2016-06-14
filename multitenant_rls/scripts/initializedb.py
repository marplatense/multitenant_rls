import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid_sqlalchemy import Session
from pyramid.scripts.common import parse_vars
from sqlalchemy import engine_from_config

from ..models.meta import Base
from ..models import Product, City, User


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    Session.configure(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with transaction.manager:

        products = [Product(id=1, name='Capsule House'), Product(id=2, name='Electric Rice Cooker'),
                    Product(id=3, name='Electric Rice Cooker'), Product(id=4, name='Silverstar 4'),
                    Product(id=5, name='Hydrojet'), Product(id=6, name='Archeological Evacuation Robot'),
                    Product(id=7, name='Time machine'), Product(id=8, name='Boat'),
                    Product(id=14, name='Motorcycle'), Product(id=19, name='Small Pirate Submarine'),
                    Product(id=21, name='Mines'), Product(id=22, name='Battle Information Building'),
                    Product(id=23, name='Team Reception Building'), Product(id=29, name='Clothing Shop Building'),
                    Product(id=30, name='Accessory Shop Building'), Product(id=36, name='Powersuit'),
                    Product(id=39, name='Mix Shop Building'), Product(id=43, name='Messerschmitt KR'),
                    Product(id=61, name='Airplane'), Product(id=67, name='Hoverbike'),
                    Product(id=69, name='Powersuit'), Product(id=80, name='Submarine'),
                    Product(id=82, name='Flying Vehicle'), Product(id=85, name='West City Police scooter'),
                    Product(id=87, name='Jet-copter'), Product(id=88, name='Skill Shop Building'),
                    Product(id=96, name='Spatiotemporal Delivery Service Building'), Product(id=103, name='Airplane'),
                    Product(id=115, name='Airplane (4 passengers)'), Product(id=116, name='Hot Air Balloon'),
                    Product(id=192, name='Airship'), Product(id=239, name='Large plane (King Castle)'),
                    Product(id=240, name='Large plane'), Product(id=333, name='Penguin 333 fridge'),
                    Product(id=339, name='Airplane'), Product(id=341, name='Flying Vehicle'),
                    Product(id=462, name='Item Shop Building'), Product(id=576, name='VTOL Plane'),
                    Product(id=673, name='Yellow Van'), Product(id=991, name='Airplane'),
                    Product(id=1138, name='Spaceship'), Product(id=2031, name='Caps Fridge'),
                    Product(id=2150, name='West City Taxi'), Product(id=2402, name='Great Saiyaman Watch'),
                    ]
        cities = [City(name='Ginger Town'), City(name='Central City'), City(name='North City'),
                  City(name='Jingle Village'), City(name='East City'), City(name='West City'),
                  City(name='Orange Star City'), City(name='South City')]
        users = []
        for city in cities:
            users.append(User(username='{}_user@example.com'.format(city.name.lower().split()[0]),
                              city=city))
        Session.add_all(products + cities + users)
