# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from printery.articles.factories import ArticleFactory
from printery.articles.models import Article


class TestArticleListView(TestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('articles:article_list')

    def test_get(self):
        # Test unauthorized user

        response = self.client.get(self.url)
        self.assertRedirects(response, '{}?next=/articles/'.format(reverse('account_login')), status.HTTP_302_FOUND, )

        User = get_user_model()

        # Test Writer Access
        user = User.objects.create(username='writer',
                                   email='writer@example.com',
                                   role=User.WRITER,
                                   password='test1234')
        self.client.force_login(user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test Editor Access
        user = User.objects.create(username='editor',
                                   email='editor@example.com',
                                   role=User.EDITOR,
                                   password='test1234')
        self.client.force_login(user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUserArticleListView(TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('articles:user_article_list')

    def test_get(self):
        # Test unauthorized user

        response = self.client.get(self.url)
        self.assertRedirects(response, '{}?next=/articles/user/'.format(reverse('account_login')),
                             status.HTTP_302_FOUND, )

        User = get_user_model()

        # Test Writer Access
        user = User.objects.create(username='writer',
                                   email='writer@example.com',
                                   role=User.WRITER,
                                   password='test1234')
        self.client.force_login(user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test Editor Access
        user = User.objects.create(username='editor',
                                   email='editor@example.com',
                                   role=User.EDITOR,
                                   password='test1234')
        self.client.force_login(user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestArticleAPIView(APITestCase):
    def setUp(self):
        super().setUp()
        self.url_list = reverse('articles:api_article-list')
        self.article = ArticleFactory.create()
        self.url_detail = reverse('articles:api_article-detail', kwargs={'pk': self.article.pk})

    def test_get(self):
        # Test unauthorized user

        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        User = get_user_model()

        # Test Writer Access
        user = User.objects.create(username='writer',
                                   email='writer@example.com',
                                   role=User.WRITER,
                                   password='test1234')
        self.client.force_login(user)

        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test Editor Access
        user = User.objects.create(username='editor',
                                   email='editor@example.com',
                                   role=User.EDITOR,
                                   password='test1234')
        self.client.force_login(user)

        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail(self):
        # Test unauthorized user

        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        User = get_user_model()

        # Test Writer Access
        user = User.objects.create(username='writer',
                                   email='writer@example.com',
                                   role=User.WRITER,
                                   password='test1234')
        self.client.force_login(user)

        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test Editor Access
        user = User.objects.create(username='editor',
                                   email='editor@example.com',
                                   role=User.EDITOR,
                                   password='test1234')
        self.client.force_login(user)

        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch(self):
        # Test unauthorized user

        response = self.client.patch(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        User = get_user_model()

        # Test Writer Access
        request_data = {
            'writer'
        }
        user = User.objects.create(username='writer',
                                   email='writer@example.com',
                                   role=User.WRITER,
                                   password='test1234')
        self.client.force_login(user)

        request_data = {
            'writer': user.pk
        }

        response = self.client.patch(self.url_detail, request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Article.objects.get(pk=self.article.pk).writer, user)

        request_data = {
            'article_url': 'http://example.com'
        }
        response = self.client.patch(self.url_detail, request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Article.objects.get(pk=self.article.pk).article_url, 'http://example.com')

        request_data = {
            'status': Article.REVIEW
        }
        response = self.client.patch(self.url_detail, request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Article.objects.get(pk=self.article.pk).status, Article.REVIEW)

        # Test Editor Access
        user = User.objects.create(username='editor',
                                   email='editor@example.com',
                                   role=User.EDITOR,
                                   password='test1234')
        self.client.force_login(user)

        request_data = {
            'status': Article.APPROVED
        }
        response = self.client.patch(self.url_detail, request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Article.objects.get(pk=self.article.pk).status, Article.APPROVED)
