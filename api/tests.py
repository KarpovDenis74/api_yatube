from django.test import TestCase
from django.test import Client
from posts.models import Post, User, Comment
from django.urls import reverse


class TestAPIPosts(TestCase):
    def setUp(self):
        self.client_on = Client()
        self.client_off = Client()
        self.user = User.objects.create(
            username='test_user', email='q@q.com')
        self.user.set_password('123')
        self.user.save()
        print(self.user.username)
        self.response = self.client_on.post(reverse('create_token'),
             data={'username': self.user.username,
             'password': self.user.password})
        self.user_2 = User.objects.create(
            username='test_user2', email='q2@q.com')
        self.user_2.set_password('1234')
        self.user_2.save()
        self.client_on.force_login(self.user)
        self.client_off.force_login(self.user_2)
        self.clients = (self.client_on, self.client_off,)

    def test_api_token(self):
        print(self.response.text)
        self.assertEqual(self.response.status_code,
            200, msg="Проверка получения токена")
        self.assertContains(
                    self.response,
                    'token',
                    count=None,
                    status_code=200,
                    msg_prefix='',
                    html=False)
