# -*- coding: utf-8 -*-
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

# get a new address to send BTC to
description = 'test-%s' % int(time.time())
address = api.get_new_address(description, None)
print "New address for payment of %s: " % description, address
# send small amount to this address
tx = api.send_btc(address, Decimal('0.001'), Decimal('0.0'))
print "0.001 BTC sent to %s, txid: %s" % (address, tx)
# Send amount, larger than available
try:
    tx = api.send_btc(address, Decimal('1000'), Decimal('0.001'))
except Exception, msg:
    print msg
    print msg.read()
