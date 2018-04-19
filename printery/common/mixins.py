# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import uuid

from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.core.exceptions import ImproperlyConfigured
from django.db import models


class DateTimeStampedModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class QueryMixin(object):
    """
    Mixin add to context query params
    """
    def get_context_data(self, **kwargs):
        context = super(QueryMixin, self).get_context_data(**kwargs)
        query_param = self.request.GET.copy()
        if 'page' in query_param.keys():
            query_param.pop('page')

        context['query_param'] = query_param.urlencode()
        return context


class ActiveTabMixin(object):
    """
    Mixin to set active tab menu
    """
    active_tab = None

    def get_active_tab(self):
        if self.active_tab is None:
            raise ImproperlyConfigured(
                "ActiveTabMixin requires either a definition of "
                "'active_tab' or an implementation of 'get_active_tab()'")
        return self.active_tab

    def get_context_data(self, **kwargs):
        context = super(ActiveTabMixin, self).get_context_data(**kwargs)
        context['active_tab'] = self.get_active_tab()
        return context


class AjaxFormResponseMixin(object):
    def form_invalid(self, form):
        response = super(AjaxFormResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxFormResponseMixin, self).form_valid(form)
        return self.render_data(response)

    def delete(self, request, *args, **kwargs):
        response = super(
            AjaxFormResponseMixin, self).delete(request, *args, **kwargs)
        return self.render_data(response)

    def render_data(self, response=None):
        if self.request.is_ajax():
            return self.render_json_object_response([self.object])
        else:
            return response


class AjaxFormMixin(AjaxResponseMixin, JSONResponseMixin, AjaxFormResponseMixin):
    pass
