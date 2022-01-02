from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from digicloud.utils.models import TrackedModel


class User(AbstractUser, TrackedModel):
    mobile = models.CharField(_('Mobile Number'), max_length=12, null=True, blank=True)
    email = models.EmailField(_('Email address'), unique=True)
    first_name = models.CharField(_('First name'), max_length=200, null=True, blank=True)
    last_name = models.CharField(_('Last name'), max_length=200, null=True, blank=True)
    REQUIRED_FIELDS = []
