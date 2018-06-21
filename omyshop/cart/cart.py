from decimal import Decimal

from config import settings
from shop.models import Product


class Cart(object):
    def __init__(self, request):
        """Initialize the cart."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_KEY)
        if not cart:
            # Assign an empty cart to the session.
            cart = self.session[settings.CART_SESSION_KEY] = {}
        self.cart = cart

    def __iter__(self):
        """Iterate over items in the cart and retrieve the products from database."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Count all items in cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Remove cart from session."""
        del self.session[settings.CART_SESSION_KEY]
        self.save()

    def add(self, product, quantity=1, update_quantity=False):
        """Add product to the cart or update its quantity."""
        product_id = str(product.id)
        if product_id not in self.cart:
            # Make an item with 0 quantity in cart for the product.
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Mark the session as "modified" to get saved."""
        self.session.modified = True

    def remove(self, product):
        """Remove the product from cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
