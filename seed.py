"""Run with: python seed.py"""
from app import create_app
from app.extensions import db
from app.models import User, Product

app = create_app()

PRODUCTS = [
    dict(name='Negroni',       category='Classic',    price=14.00,
         description='Gin, Campari, sweet vermouth. Stirred, served on the rocks with an orange peel.'),
    dict(name='Margarita',     category='Classic',    price=13.00,
         description='Blanco tequila, triple sec, fresh lime juice, salted rim.'),
    dict(name='Old Fashioned', category='Classic',    price=15.00,
         description='Bourbon, Angostura bitters, sugar, orange twist.'),
    dict(name='Espresso Martini', category='Modern',  price=16.00,
         description='Vodka, fresh espresso, coffee liqueur, sugar syrup. Shaken hard.'),
    dict(name='Aperol Spritz', category='Spritz',     price=12.00,
         description='Aperol, prosecco, soda water, orange slice.'),
    dict(name='Moscow Mule',   category='Refreshing', price=13.00,
         description='Vodka, ginger beer, fresh lime juice, served in a copper mug.'),
]

with app.app_context():
    db.drop_all()
    db.create_all()

    staff = User(name='Admin', email='admin@cocktails.com', is_staff=True)
    staff.set_password('admin1234')
    db.session.add(staff)

    for p in PRODUCTS:
        db.session.add(Product(**p))

    db.session.commit()
    print(f'Seeded {len(PRODUCTS)} products and 1 staff user (admin@cocktails.com / admin1234).')
