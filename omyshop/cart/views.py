from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from coupons.forms import CouponApplyForm
from shop.recommender import Recommender
from .forms import CartAddProductForm
from shop.models import Product
from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    # Iterate each item in cart to add form to update quantity.
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True})
    coupon_apply_form = CouponApplyForm()

    r = Recommender()
    cart_products = [item['product'] for item in cart]
    recommend_products = r.suggest_products(cart_products)
    return render(request, 'cart/detail.html',
                  {'cart': cart,
                   'coupon_apply_form': coupon_apply_form,
                   'recommend_products':recommend_products})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart-detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart-detail')
