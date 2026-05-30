from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Product, Order, OrderItem

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')


# ── Helpers ────────────────────────────────────────────────────────────────

def get_cart():
    """Return cart from session as {product_id (int): quantity}."""
    return {int(k): v for k, v in session.get('cart', {}).items()}


def save_cart(cart):
    session['cart'] = {str(k): v for k, v in cart.items()}
    session.modified = True


def cart_summary():
    """Return (list of dicts, total) for the current cart."""
    cart = get_cart()
    if not cart:
        return [], 0

    products = {p.id: p for p in Product.query.filter(Product.id.in_(cart)).all()}
    items = []
    total = 0
    for pid, qty in cart.items():
        product = products.get(pid)
        if product and product.is_available:
            subtotal = product.price * qty
            items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
            total += subtotal
    return items, total


# ── Routes ─────────────────────────────────────────────────────────────────

@cart_bp.route('/')
@login_required
def view():
    items, total = cart_summary()
    return render_template('cart/cart.html', items=items, total=total)


@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add(product_id):
    product = db.session.get(Product, product_id)
    if not product or not product.is_available:
        flash('That product is not available.', 'error')
        return redirect(url_for('menu.index'))

    cart = get_cart()
    cart[product_id] = cart.get(product_id, 0) + 1
    save_cart(cart)
    flash(f'{product.name} added to cart.', 'success')
    return redirect(request.referrer or url_for('menu.index'))


@cart_bp.route('/remove/<int:product_id>', methods=['POST'])
@login_required
def remove(product_id):
    cart = get_cart()
    cart.pop(product_id, None)
    save_cart(cart)
    return redirect(url_for('cart.view'))


@cart_bp.route('/update', methods=['POST'])
@login_required
def update():
    cart = get_cart()
    for key, value in request.form.items():
        if key.startswith('qty_'):
            try:
                pid = int(key[4:])
                qty = int(value)
                if qty > 0:
                    cart[pid] = qty
                else:
                    cart.pop(pid, None)
            except (ValueError, KeyError):
                pass
    save_cart(cart)
    return redirect(url_for('cart.view'))


@cart_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    items, total = cart_summary()
    if not items:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('cart.view'))

    if request.method == 'POST':
        address = request.form.get('address', '').strip()
        if not address:
            flash('Please enter a delivery address.', 'error')
            return render_template('cart/checkout.html', items=items, total=total)

        order = Order(
            user_id=current_user.id,
            delivery_address=address,
            total_price=total,
            status=Order.STATUS_PENDING,
        )
        db.session.add(order)
        db.session.flush()  # get order.id before committing

        for item in items:
            db.session.add(OrderItem(
                order_id=order.id,
                product_id=item['product'].id,
                quantity=item['quantity'],
                unit_price=item['product'].price,
            ))

        db.session.commit()
        save_cart({})  # clear cart

        flash('Order placed successfully!', 'success')
        return redirect(url_for('cart.confirmation', order_id=order.id))

    return render_template('cart/checkout.html', items=items, total=total)


@cart_bp.route('/confirmation/<int:order_id>')
@login_required
def confirmation(order_id):
    order = db.session.get(Order, order_id)
    if not order or order.user_id != current_user.id:
        flash('Order not found.', 'error')
        return redirect(url_for('menu.index'))
    return render_template('cart/confirmation.html', order=order)
