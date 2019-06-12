# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# User model
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
import six
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


@six.python_2_unicode_compatible
class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        app_label = "main"
        db_table = "auth_user"
        abstract = False
        ordering = ["username"]

    username = models.CharField(_('username'), max_length=75, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            RegexValidator(r'^[\w.@+-]+$', _('Enter a valid username.'), 'invalid')
        ])

    def __str__(self):
        return self.username
