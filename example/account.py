"""\
Send a very small amount of BTC to yourself
"""
from decimal import Decimal

import os
import time
import random

from mtgoxexp import MtGoxAccess
from mtgoxexp import Account

random.seed(time.time())

dirname = os.path.dirname(__file__)
MTGOX_KEY = file(os.path.join(dirname, 'mtgox-key.secret')).read().strip()
MTGOX_SECRET = file(os.path.join(dirname, 'mtgox-secret.secret')).read().strip()

auth = MtGoxAccess(MTGOX_KEY, MTGOX_SECRET)
api = Account(auth)

from pprint import PrettyPrinter

pp = PrettyPrinter(indent=2)

# get account info
#pp.pprint(api.info())

# Balance
for currency in ('BTC', 'EUR'):
    print currency
    print 'balance:   ', api.balance(currency)
    print 'available: ', api.available(currency)
