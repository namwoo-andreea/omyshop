import braintree
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from orders.models import Order


def payment_process(request):
    # 1. A client token is generated using braintree python module.
    # This token will be used to instantiate the braintree javascript client; it is not payment token.
    # 2. The view renders payment template. The template load braintree javascript SDK using client token
    # and generate iframe with the hosted payment form fields.
    # 3. User enter their credit card details and submit the form. A payment token nonce is generated with
    # braintree javascript client. We send the token to our view with a POST request.
    # 4. Our view use the token to generate transcation using braintree python module.

    order_id = request.session['order_id']
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce', None)
        result = braintree.Transaction.sale({
            'amount': '{}'.format(order.get_total_cost()),
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')

    else:
        # Generate client token
        client_token = braintree.ClientToken.generate()
        return render(request, 'payment/process.html',
                      {'order': order,
                       'client_token': client_token})


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
