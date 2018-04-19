from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):
    WRITER = 'writer'
    EDITOR = 'editor'
    ROLES = (
        (WRITER, _('Writer')),
        (EDITOR, _('Editor')),
    )

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)

    role = models.CharField(max_length=255,
                            choices=ROLES,
                            default=WRITER,
                            verbose_name=_('Role'))

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    @property
    def is_writer(self):
        return self.role == self.WRITER

    @property
    def is_editor(self):
        return self.role == self.EDITOR
