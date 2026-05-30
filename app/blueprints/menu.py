from flask import Blueprint, render_template
from app.models import Product

menu_bp = Blueprint('menu', __name__)


@menu_bp.route('/')
def index():
    products = Product.query.filter_by(is_available=True).all()
    return render_template('index.html', products=products)
