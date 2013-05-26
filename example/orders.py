# -*- coding: utf-8 -*-
"""\
Add an order
View all open orders
cancel the order
"""
from decimal import Decimal

import os
import time
import random

from mtgoxexp import MtGoxAccess
from mtgoxexp import Trade

random.seed(time.time())

dirname = os.path.dirname(__file__)
MTGOX_KEY = file(os.path.join(dirname, 'mtgox-key.secret')).read().strip()
MTGOX_SECRET = file(os.path.join(dirname, 'mtgox-secret.secret')).read().strip()

auth = MtGoxAccess(MTGOX_KEY, MTGOX_SECRET)
api = Trade(auth)

from pprint import PrettyPrinter

pp = PrettyPrinter(indent=2)

# TRADE!
market = 'BTCEUR'

# Open Orders
orders = api.orders(market)
print len(orders), "open orders"

if not orders:
    order_id = api.add(market, 'bid', Decimal('1000'), Decimal('10'))
    print "added:", order_id

orders = api.orders(market)
pp.pprint(orders)

for order in orders:
    order_id = order['oid']
    api.cancel(market, order_id)
    print "cancelled:", order_id
