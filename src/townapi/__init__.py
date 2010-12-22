from ext import ClientBase
from ext import oauth2
from oauth2 import urlparse, parse_qsl 
from config import *
import json

CONSUMER = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)

class TownApi(ClientBase):
    def __init__(self, token_key=None, token_secret=None, cache=None,
                 timeout=None, proxy_info=None):
        token = None
        if token_key:
            token = oauth2.Token(token_key, token_secret)
        ClientBase.__init__(self, CONSUMER, token, cache, timeout, proxy_info)
    
    def _parse_token_response(self, response):
        resp, content = response
        if resp['status'] != '200': 
            raise Exception('%s HTTP Error' % resp['status'])
        
        result = dict(parse_qsl(content))
        return result['oauth_token'], result['oauth_token_secret']
    
    def _parse_json_response(self, response):
        resp, content = response
        if resp['status'] != '200':
            raise Exception('%s HTTP Error' % resp['status'])
        return json.loads(content)        
    
    def get_oauth_request_token(self, callback):
        self.set_callback(callback)
        response = self.request(REQUEST_TOKEN_URL, "GET")
        self.callback = None
        return self._parse_token_response(response)
    
    def get_oauth_access_token(self, verifier):
        self.token.set_verifier(verifier)
        response = self.request(ACCESS_TOKEN_URL, "POST")
        return self._parse_token_response(response)
    
    def get_users_show(self, user_id=None):
        uri = SERVICE_PROVIDER_URL + "/users/show/"
        if user_id:
            uri += user_id
        response = self.request(uri, "GET")
        return self._parse_json_response(response)