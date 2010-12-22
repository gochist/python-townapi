#-*- coding: utf-8 -*-
from ext import ClientBase
from ext import oauth2
from oauth2 import urlparse, parse_qsl 
from config import *
from urllib import urlencode
import json

CONSUMER = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)

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
    
    # check token
    username = check_access_token(key, secret)
    print username, "님 반갑습니다. 인증에 성공했습니다."
    return ret


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
        if type(obj) is dict:
            if obj.get('status', 'ok') == 'error':
                raise Exception(obj['message'])
        return obj
    
    def _get(self, uri, param=None):
        if not uri.startswith(SERVICE_PROVIDER_URL):
            uri = SERVICE_PROVIDER_URL + uri
        if param:
            if not uri.endswith('?'):
                uri += '?'
            uri += urlencode(param)
        response = self.request(uri, "GET")
        return self._parse_json_response(response)

    def _post(self, uri, params):
        def to_utf8(buf):
            if type(buf) is unicode:
                return buf.encode('utf8')
            return buf
        
        if not uri.startswith(SERVICE_PROVIDER_URL):
            uri = SERVICE_PROVIDER_URL + uri
            
        if params:
            params = dict([(k, to_utf8(v)) for k, v in params.iteritems()])
        
        body = urlencode(params)
        response = self.request(uri, "POST", body)
        
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
        if user_id:
            return self._get("/users/show/%s" % user_id)
        return self._get("/users/show")
    
    def get_users_lookup(self, user_id):
        return self._get("/users/lookup?", {'user_id': user_id})

    def get_users_search(self, q):
        return self._get("/users/search?", {'q': q})
    
    def get_boards_favorite(self):
        return self._get("/boards/favorite")
    
    def get_boards_lookup(self, board_id):
        return self._get("/boards/lookup", {'board_id': board_id})
    
    def get_articles_list(self, board_id, page=0, per_page=20, q=""):
        params = {'page':page, 'per_page':per_page, 'q':q}
        return self._get("/articles/list/%s" % board_id, params)
    
    def get_articles_show(self, board_id, article_id):
        return self._get("/articles/show/%s/%s" % (board_id, article_id))
    
    def get_favorites_list(self):
        return self._get("/favorites/list")
    
    def post_articles_create(self, board_id, title, message):
        uri = "/articles/create/%s" % board_id
        params = {'title': title, 'message': message}
        return self._post(uri, params)
    
    def post_comments_create(self, board_id, article_id, message):
        uri = "/comments/create/%s/%s" % (board_id, article_id)
        params = {'message': message}
        return self._post(uri, params)

        

