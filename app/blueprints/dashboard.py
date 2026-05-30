from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Order
from app.email import send_order_delivered

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

VALID_STATUSES = [
    Order.STATUS_PENDING,
    Order.STATUS_CONFIRMED,
    Order.STATUS_DELIVERING,
    Order.STATUS_DELIVERED,
    Order.STATUS_CANCELLED,
]


def staff_required(fn):
    """Decorator: 403 for non-staff users."""
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_staff:
            abort(403)
        return fn(*args, **kwargs)
    return wrapper


@dashboard_bp.route('/orders')
@login_required
@staff_required
def orders():
    status_filter = request.args.get('status', '')
    query = Order.query.order_by(Order.created_at.desc())
    if status_filter in VALID_STATUSES:
        query = query.filter_by(status=status_filter)

    all_orders = query.all()

    counts = {s: Order.query.filter_by(status=s).count() for s in VALID_STATUSES}
    counts['all'] = Order.query.count()

    return render_template('dashboard/orders.html',
                           orders=all_orders,
                           counts=counts,
                           status_filter=status_filter,
                           valid_statuses=VALID_STATUSES)


@dashboard_bp.route('/orders/<int:order_id>')
@login_required
@staff_required
def order_detail(order_id):
    order = db.session.get(Order, order_id)
    if not order:
        abort(404)
    return render_template('dashboard/order_detail.html',
                           order=order,
                           valid_statuses=VALID_STATUSES)


@dashboard_bp.route('/orders/<int:order_id>/status', methods=['POST'])
@login_required
@staff_required
def update_status(order_id):
    order = db.session.get(Order, order_id)
    if not order:
        abort(404)

    new_status = request.form.get('status')
    if new_status not in VALID_STATUSES:
        flash('Invalid status.', 'error')
        return redirect(url_for('dashboard.order_detail', order_id=order_id))

    order.status = new_status
    db.session.commit()

    if new_status == Order.STATUS_DELIVERED:
        send_order_delivered(order)

    flash(f'Order #{order.id} updated to {order.status_label}.', 'success')
    return redirect(url_for('dashboard.order_detail', order_id=order_id))
