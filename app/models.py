from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    name       = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_staff   = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    orders = db.relationship('Order', back_populates='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class Product(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price       = db.Column(db.Numeric(8, 2), nullable=False)
    category    = db.Column(db.String(50))
    image_url   = db.Column(db.String(300))
    is_available = db.Column(db.Boolean, default=True, nullable=False)

    order_items = db.relationship('OrderItem', back_populates='product')

    def __repr__(self):
        return f'<Product {self.name}>'


class Order(db.Model):
    STATUS_PENDING    = 'pending'
    STATUS_CONFIRMED  = 'confirmed'
    STATUS_DELIVERING = 'out_for_delivery'
    STATUS_DELIVERED  = 'delivered'
    STATUS_CANCELLED  = 'cancelled'

    id               = db.Column(db.Integer, primary_key=True)
    user_id          = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status           = db.Column(db.String(20), default=STATUS_PENDING, nullable=False)
    delivery_address = db.Column(db.Text, nullable=False)
    total_price      = db.Column(db.Numeric(10, 2), nullable=False)
    created_at       = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at       = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                                 onupdate=lambda: datetime.now(timezone.utc))

    user  = db.relationship('User', back_populates='orders')
    items = db.relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')

    @property
    def status_label(self):
        return self.status.replace('_', ' ').title()

    def __repr__(self):
        return f'<Order {self.id} {self.status}>'


class OrderItem(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    order_id   = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity   = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(8, 2), nullable=False)

    order   = db.relationship('Order', back_populates='items')
    product = db.relationship('Product', back_populates='order_items')

    @property
    def subtotal(self):
        return self.unit_price * self.quantity

    def __repr__(self):
        return f'<OrderItem {self.product_id} x{self.quantity}>'
