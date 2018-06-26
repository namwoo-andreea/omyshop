import weasyprint
from celery.task import task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from io import BytesIO

from config import settings
from orders.models import Order


@task
def send_invoice(order_id):
    """
    Send an email with invoice pdf when payment is successfully done.
    """
    order = Order.objects.get(id=order_id)
    subject = 'O My Shop - Invoice no. {}'.format(order.id)
    message = 'Thank you for attention, ' \
              'we send the invoice for you recent order.'
    email = EmailMessage(subject,
                         message,
                         'admin@omyshop.com',
                         [order.email])
    # Generate PDF
    html = render_to_string('orders/invoice.html',
                            {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(
        settings.STATIC_ROOT + 'css/invoice.css')]
    weasyprint.HTML(string=html).write_pdf(out,
                                           stylesheets=stylesheets)
    # Attach PDF
    email.attach('order_{}.pdf'.format(order.id),
                 out.getvalue(),
                 'application/pdf')
    return email.send()