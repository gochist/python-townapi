#-*- coding: utf-8 -*-
from ext import ClientBase
from ext import oauth2
from oauth2 import urlparse, parse_qsl 
from config import *
from urllib import urlencode
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
        obj = json.loads(content)
        if type(obj) == dict:
            if obj.get('status', 'ok') == 'error':
                raise Exception(obj['message'])
        return obj
    
    def _get(self, uri, param=None):
        if param:
            if not uri.endswith('?'):
                uri += '?'
            uri += urlencode(param)
        response = self.request(uri, "GET")
        return self._parse_json_response(response)
    
    def get_oauth_request_token(self, callback):
        self.set_callback(callback)
        response = self.request(REQUEST_TOKEN_URL, "GET")
        self.callback = None
        return self._parse_token_response(response)
    
    def post_oauth_access_token(self, verifier):
        self.token.set_verifier(verifier)
        response = self.request(ACCESS_TOKEN_URL, "POST")
        return self._parse_token_response(response)
    
    def get_users_show(self, user_id=None):
        uri = SERVICE_PROVIDER_URL + "/users/show/"
        return self._get(uri)
    
    def get_users_lookup(self, user_id):
        uri = SERVICE_PROVIDER_URL + "/users/lookup?"
        return self._get(uri, {'user_id': user_id})

    def get_users_search(self, q):
        uri = SERVICE_PROVIDER_URL + "/users/search?"
        return self._get(uri, {'q': q})

def check_access_token(key, secret):
    "access_token이 유효한 경우 username을 반환한다."
    api = TownApi(key, secret)
    try:
        user = api.get_users_show()
    except:
        return False
    return user['name']

def init_access_token():
    ret = None
    # request request_token
    api = TownApi()
    key, secret = api.get_oauth_request_token("oob")
    url = "%s?oauth_token=%s" % (AUTHORIZE_URL, key)
    print "다음 URL을 방문해서 PIN을 발급받으세요.\n%s" % url
    
    # request access_token
    while(not ret):
        verifier = raw_input("PIN을 입력하세요:")
        api = TownApi(key, secret)
        try:
            key, secret = api.post_oauth_access_token(verifier)
            ret = key, secret
        except:
            print "인증에 실패했습니다."
    
    # get user
    username = check_access_token(key, secret)
    print username, "님 반갑습니다. 인증에 성공했습니다."
    return ret
