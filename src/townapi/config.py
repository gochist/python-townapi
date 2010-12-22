#-*- coding: utf-8 -*-
CONSUMER_KEY = "consumer_key"
CONSUMER_SECRET = "consumer_secret"

CALLBACK_URL = "http://localhost:9000/accounts/callback"
SERVICE_PROVIDER_URL = "http://devapi.caucse.net"

REQUEST_TOKEN_URL = SERVICE_PROVIDER_URL + "/oauth/request_token"
ACCESS_TOKEN_URL = SERVICE_PROVIDER_URL + "/oauth/access_token"
AUTHORIZE_URL = SERVICE_PROVIDER_URL + "/oauth/authorize"