# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from django.views.generic import ListView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from printery.common.mixins import QueryMixin
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from .models import Article
from .serializers import ArticleSerializer


class ArticleListView(LoginRequiredMixin, QueryMixin, ListView):
    model = Article
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_writer:
            return queryset.filter(status=Article.NEW, writer__isnull=True)
        elif self.request.user.is_editor:
            return queryset.filter(status=Article.REVIEW, editor__isnull=True)
        else:
            return queryset.none()


class UserArticleListView(LoginRequiredMixin, QueryMixin, ListView):
    model = Article
    template_name = 'articles/user_article_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_writer:
            return queryset.filter(writer=self.request.user).order_by('-status')
        elif self.request.user.is_editor:
            return queryset.filter(editor=self.request.user).order_by('-status')
        else:
            return queryset.none()


class ArticleAPIView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    http_method_names = ['get', 'patch', 'head', 'options', 'trace']

    def perform_update(self, serializer):
        messages.add_message(self.request, messages.SUCCESS, _('Article was successfully updated.'))
        serializer.save()
