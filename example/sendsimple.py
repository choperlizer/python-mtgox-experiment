"""\
Send a very small amount of BTC to yourself
"""
from decimal import Decimal

from mtgoxexp import MtGoxAccess
from mtgoxexp import Trade


import os
dirname = os.path.dirname(__file__)
MTGOX_KEY = file(os.path.join(dirname, 'mtgox-key.secret')).read().strip()
MTGOX_SECRET = file(os.path.join(dirname, 'mtgox-secret.secret')).read().strip()

auth = MtGoxAccess(MTGOX_KEY, MTGOX_SECRET)
api = Trade(auth)

api.send_btc('1ByFDtUWowVep6NpvCh6rqATUvbhgmX4U2',
             Decimal('0.001'))
