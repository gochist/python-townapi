#-*- coding: utf-8 -*-
from townapi import TownApi, init_access_token, check_access_token
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
        
    def test_get_boards_lookup(self):
        board_id = "board_freeboard,board_alumni99,photo_alumni99"
        boards = self.api.get_boards_lookup(board_id)
        ids = [board['board_id'] for board in boards]
        self.assertTrue('board_freeboard' in ids)
        self.assertTrue('photo_alumni99' in ids)
        
    def test_get_boards_favorite(self):
        boards = self.api.get_boards_favorite()
        ids = [board['board_id'] for board in boards]
        self.assertTrue('board_freeboard' in ids)
        
    def test_get_articles_list(self):
        board_id = "board_alumni99"
        response = self.api.get_articles_list(board_id)
        articles = response['articles']
        listinfo = response['listinfo']
        self.assertEqual(listinfo['board_id'], board_id)
        self.assertEqual(articles[0]['board_id'], board_id)
        
    def test_get_articles_show(self):
        board_id = "board_alumni99"
        article_id = 100
        article = self.api.get_articles_show(board_id, article_id)
        self.assertEqual(article['board_id'], board_id)
        self.assertEqual(article['id'], article_id)
        
    def test_get_favorites(self):
        favorites = self.api.get_favorites_list()
        self.assertEqual(type(favorites), list)
        
    def test_post_articles_create(self):
        board_id = "board_alumni99"
        title = u"제목?"
        message = u"메시지를 써볼까요....\n\n흐음... 줄바꾸기는?"
        response = self.api.post_articles_create(board_id, title, message)
        status = response['status']
        article = response['article']
        self.assertEqual(status, 'ok')
        self.assertEqual(article['board_id'], board_id)
        self.assertEqual(article['title'], title)
        
    def test_post_comments_create(self):
        board_id = "board_alumni99"
        article_id = 100
        message = u'커멘트 테스트 하는 중....'
        response = self.api.post_comments_create(board_id, article_id, message)
        status = response['status']
        comment = response['comment']
        self.assertEqual(status, 'ok')
        self.assertEqual(comment['board_id'], board_id)
        self.assertEqual(comment['content'], message)
        
if __name__ == '__main__':
    access_token = ('28767d0e02cf46d69eefb6e2a8b550f9',
                    'a780c01643a1456bbebdb797b22ebcb3')
    username = check_access_token(*access_token)
    if not username:
        access_token = init_access_token()
        print "access_token =", access_token
    unittest.main()
