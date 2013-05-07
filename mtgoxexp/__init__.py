"""\
2013-05-07 R.R. Nederhoed

This module implements only the calls needed to receive, buy, sell and send BTC.
It does not aspire to build an implementation of the complete API.

Webshop
* create a BTC address with IPN for payment notification
* on payment, we want to sell the BTC on the market
Bitcoin selling
* buy BTC 
* send it to the customer

In both cases we need the be able to request pricing info.
"""
import time
import urllib
import urllib2
import json
from decimal import Decimal

import hmac
from hashlib import sha512
import base64


def satoshi2decimal(satoshis):
    """Convert an integer Bitcoin amount to decimal
    >>> v = 1  # 1 satoshi
    >>> satoshi2decimal(v)
    Decimal('1E-8')
    """
    return Decimal("%.8f"%(satoshis/100000000.))

def decimal2satoshi(value):
    """Convert a decimal value to satoshis
    >>> v = Decimal('0.00000001')  # 1 satoshi
    >>> decimal2satoshi(v)
    1L
    """
    return long(value*100000000)


class MtGoxAccess(object):
    """Authentication to the API """
    url_api = "https://data.mtgox.com/api/2/"
    
    def __init__(self, key, secret, client="Experimental Bitcoin Client v0.1"):
        self._key = key
        self._secret = secret
        self._client = client
    
    def _get_signature(self, path, data):
        hash_data = path + chr(0) + data
        h = hmac.new(base64.b64decode(self._secret), hash_data, sha512)
        return base64.b64encode(str(h.digest()))
    
    def call(self, path, data):
        """ """
        url = MtGoxAccess.url_api + path
        if data is None:
            data = {'nonce' : time.time()}
        else:
            data.update({'nonce' : time.time()})
        # Encode
        data = urllib.urlencode(data)
        request = urllib2.Request(url, data)
        # Sign
        request.add_header("User-Agent", self._client)
        request.add_header('Rest-Key', self._key)
        request.add_header('Rest-Sign', self._get_signature(path, data))
        # Retrieve info
        result = json.load(urllib2.urlopen(request))
        if result['result'] == 'success':
            return result['return']
        else:
            raise ValueError(result['error'])

class Trade(object):
    """ """
    def __init__(self, mtgox_access):
        """Trade on MtGox """
        self.mtgox = mtgox_access
    
    def _request(self, path, data):
        try:
            return self.mtgox.call(path, data)
        except Exception, msg:
            print msg

    def send_btc(self, address, amount):
        """Send the given amount to the given address 
        address
        amount as Decimal
        (fee_int, no_instant, green)
        Note: You are not able to perform this method if you have enabled 
        Two-Factor authentication for withdrawals.
        
        We default to no_instant, not green with a fee of 0.0005.
        """
        path = "money/bitcoin/send_simple"
        # Convert Decimal amount to int
        data = {
            'address': address,
            'amount_int': decimal2satoshi(amount),
            'fee_int': decimal2satoshi(Decimal('0.0000')),
            'no_instant': False,
            'green': False,
        }
        print data
        return self._request(path, data)

    def add(self, todo):
        """Place order """

class MtGoxIPN(object):
    """Like WalletBit """
    url_api = "https://mtgox.com/api/1"
    
    def __init__(self, key, secret):
        self._key = key
        self._secret = secret
    
    def _get_signature(self, data):
        h = hmac.new(base64.b64decode(self._secret), data, sha512)
        return base64.b64encode(str(h.digest()))
    
    def _request_json(self, url, data):
        """ """
        if data is None:
            data = {'nonce' : time.time()}
        else:
            data.update({'nonce' : time.time()})
        # Encode
        data = urllib.urlencode(data)
        request = urllib2.Request(url, data)
        # Sign
        request.add_header("User-Agent", "Bitbank Client v0.1")
        request.add_header('Rest-Key', self._key)
        request.add_header('Rest-Sign', self._get_signature(data))
        # Retrieve info
        result = json.load(urllib2.urlopen(request))
        if result['result'] == 'success':
            return result['return']
        else:
            raise ValueError(result['error'])

    def get_new_address(self, description, ipn_url):
        """Request a new btc_address 
        Description should be unique for a new address to be created.
        """
        call = "/generic/bitcoin/address"
        data = {'description': description, 'ipn': ipn_url}
        result = self._request_json(MtGoxIPN.url_api+call, data)
        return result['addr']
    

if __name__ == "__main__":
    import doctest
    doctest.testmod()