from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')


@cart_bp.route('/')
@login_required
def view():
    return render_template('cart/cart.html')


@cart_bp.route('/add/<int:product_id>')
@login_required
def add(product_id):
    flash('Cart coming soon!', 'info')
    return redirect(url_for('menu.index'))
