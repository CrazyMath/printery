# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from printery.common.mixins import UUIDModel, DateTimeStampedModel

User = get_user_model()


@python_2_unicode_compatible
class Article(UUIDModel, DateTimeStampedModel):
    NEW = 'new'
    REVIEW = 'review'
    APPROVED = 'approved'

    STATUSES = (
        (NEW, _('New')),
        (REVIEW, _('Review')),
        (APPROVED, _('Approved')),
    )
    status = models.CharField(max_length=255,
                              verbose_name=_('Status'),
                              choices=STATUSES,
                              default=NEW)
    article_url = models.URLField(verbose_name=_('Article Url'),
                                  help_text=_('Url should point to google docs.'),
                                  blank=True, null=True)
    title = models.CharField(max_length=255,
                             verbose_name=_('Title'))
    editor = models.ForeignKey(User,
                               related_name='edited_articles',
                               verbose_name=_('Editor'),
                               null=True)
    writer = models.ForeignKey(User,
                               related_name='written_articles',
                               verbose_name=_('Writer'),
                               null=True)

    def __str__(self):
        return self.title

    def clean(self):
        if not self.article_url and (self.status in [self.REVIEW, self.APPROVED]):
            raise ValidationError(_('Article can\'t be approved with empty article url.'))
