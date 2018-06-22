from django.shortcuts import render, redirect
from django.urls import reverse

from cart.cart import Cart
from .tasks import order_created
from .models import OrderItem
from .forms import OrderCreateForm


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # Clear the cart.
            cart.clear()
            order_created.delay(order.id)
            # Set the order in session.
            request.session['order_id'] = order.id
            # Redirect to payment process.
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request, 'order/create.html',
                  {'cart': cart,
                   'form': form})
