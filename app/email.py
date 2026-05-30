import logging
from flask import render_template, current_app
from flask_mail import Message
from app.extensions import mail

logger = logging.getLogger(__name__)


def _send(subject, recipient, template, **kwargs):
    """Render an HTML email template and send it. Silently logs on failure."""
    try:
        body = render_template(template, **kwargs)
        msg = Message(subject=subject, recipients=[recipient], html=body)
        mail.send(msg)
    except Exception as exc:
        # Never let email errors bubble up and break the user-facing request.
        logger.warning('Failed to send email to %s: %s', recipient, exc)


def send_order_confirmed(order):
    _send(
        subject=f'Order #{order.id} confirmed — Cocktail Delivery',
        recipient=order.user.email,
        template='emails/order_confirmed.html',
        order=order,
    )


def send_order_delivered(order):
    _send(
        subject=f'Your order #{order.id} has been delivered!',
        recipient=order.user.email,
        template='emails/order_delivered.html',
        order=order,
    )
