from django.test import TestCase, Client
import unittest
from http import HTTPStatus
from accounts.models import Account
from posts.models import Post, Comment
from posts.serializers import CommentSerializer

class PostAPITestCase(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_list_exists(self):
        """Проверка доступности списка рецептов"""
        response = self.guest_client.get('/api/posts/')
        self.assertEqual(response.status_code, HTTPStatus.OK)


class MyTestCase(unittest.TestCase):

    def test_dummy(self):
        self.assertEqual(2+2,4)

# class CommentTest(TestCase):
#     def SetUp(self):
#         author = Account.objects.get(id=2)
#         post = Post.objects.get(id=2)
#         Comment.objects.create(
#             post=post, author=author, text='text35'
#         )
#
#     def test_comment(self):
#         comment_1 = Comment.objects.get(text='text35')
#         self.assertEquals(comment_1.text, text35)

class PostTest(TestCase):
    # def SetUp(self):
    #     author = Account.objects.get(id=2)
    #     Post.objects.create(
    #         name='kartina', text='text', author=author
    #     )

    def test_post(self):
        post1 = Post.objects.get(name='Почтальон')
        self.assertEquals(post1.name, 'Почтальон')
