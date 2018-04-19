# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url, include
from rest_framework import routers

from .views import ArticleListView, UserArticleListView, ArticleAPIView

router = routers.DefaultRouter()
router.register(r'api/articles', ArticleAPIView, base_name='api_article')

urlpatterns = [
    url(r'^', include(router.urls)),

    url(
        regex=r'^articles/$',
        view=ArticleListView.as_view(),
        name='article_list'
    ),
    url(
        regex=r'^articles/user/$',
        view=UserArticleListView.as_view(),
        name='user_article_list'
    ),
]
