#-*- coding: utf-8 -*-
from townapi import TownApi, config, init_access_token, check_access_token
import unittest

class TestTownApi(unittest.TestCase):
    def setUp(self):
        self.api = TownApi(*access_token)
        
    def test_get_users_show(self):
        user = self.api.get_users_show("gochi")
        self.assertEqual(user['name'], u'이덕준')
        
    def test_get_users_lookup(self):
        userlist = self.api.get_users_lookup("gochi,reset")
        names = [user['name'] for user in userlist]
        self.assertTrue(u"이덕준" in names)
        self.assertTrue(u"강석천" in names)
        self.assertFalse(u"박종필" in names)
        
    def test_get_users_search(self):
        # 99학번 중 이름에 '준'이 들어가는 학우 검색 
        q = "99 준"
        userlist = self.api.get_users_search(q)
        names = [user['name'] for user in userlist]
        self.assertTrue(u'이덕준' in names)
        self.assertFalse(u'박종필' in names)
        
        # 15학번 검색! 2015년 이전까지는 없을테니, Exception.
        q = "15"
        self.assertRaises(Exception, self.api.get_users_search, (q))
        
if __name__ == '__main__':
    access_token = ('8f64c38e8c884a97b76dbd3384a57160',
                    '77a9ce2fbf004386be753b39292f8272')
    if not check_access_token(*access_token):
        access_token = init_access_token()
        print "access_token:", access_token
    unittest.main()
