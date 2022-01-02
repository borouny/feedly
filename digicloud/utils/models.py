from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TrackedModel(models.Model):
    class Meta:
        abstract = True

    is_active = models.BooleanField(verbose_name=_('Active?'), default=True)

    created = models.DateTimeField(verbose_name=_('Creation Time'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Update Time'), auto_now=True)
    removed = models.DateTimeField(verbose_name=_('Remove Time'), blank=True, null=True)

    def delete(self, purge=False, using=None, keep_parents=False):
        if purge:
            return super(TrackedModel, self).delete(using, keep_parents)
        else:
            self.removed = timezone.now()
            self.is_active = False
            self.save()

    def save(self, *args, **kwargs):
        now = timezone.now()
        if not self.id:
            self.created = now
        self.modified = now
        return super(TrackedModel, self).save(*args, **kwargs)
