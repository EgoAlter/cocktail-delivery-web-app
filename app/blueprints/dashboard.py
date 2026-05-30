from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Order

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/orders')
@login_required
def orders():
    if not current_user.is_staff:
        return render_template('index.html'), 403
    all_orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('dashboard/orders.html', orders=all_orders)
