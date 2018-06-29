import redis

from config import settings
from shop.models import Product

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class Recommender(object):
    def get_product_key(self, id):
        return 'product:{}:purchased_with'.format(id)

    def products_bought(self, products):
        """Update rank of products in sorted set"""
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                if product_id != with_id:
                    r.zincrby(self.get_product_key(product_id),
                              with_id,
                              amount=1)

    def suggest_products(self, products, max_result=6):
        """Suggest product as many as max result"""
        product_ids = [p.id for p in products]
        # Only one product
        if len(products) == 1:
            suggestions = r.zrange(self.get_product_key(product_ids[0]),
                                   0, -1, desc=True)[:max_result]
        else:
            # Multiple products, combine scores of all products
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = 'tmp_{}'.format(flat_ids)
            # Store sorted sets in a temporary key
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            # Remove ids for the products already in cart or order
            r.zrem(tmp_key, *product_ids)
            suggestions = r.zrange(tmp_key,
                                   0, -1, desc=True)[:max_result]
            # Remove temporary key
            r.delete(tmp_key)
        suggested_product_ids = [int(id) for id in suggestions]
        suggested_products = Product.objects.filter(id__in=suggested_product_ids)
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.value_list(id, flat=True):
            r.delete(self.get_product_key(id))
