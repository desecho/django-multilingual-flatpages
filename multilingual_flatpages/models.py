from __future__ import unicode_literals

from django.contrib.sites.models import Site
from django.db import models
from django.core.urlresolvers import get_script_prefix
from django.utils.encoding import iri_to_uri, python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from hvad.models import TranslatableModel, TranslatedFields
from hvad.manager import TranslationManager


@python_2_unicode_compatible
class FlatPage(TranslatableModel):
    name = models.CharField(_('Name'), max_length=100)
    translations = TranslatedFields(
        url=models.CharField(_('URL'), max_length=100, db_index=True),
        title=models.CharField(_('title'), max_length=200),
        content=models.TextField(_('content'), blank=True),
    )
    enable_comments = models.BooleanField(_('enable comments'), default=False)
    template_name = models.CharField(
        _('template name'),
        max_length=70,
        blank=True,
        help_text=_(
            "Example: 'flatpages/contact_page.html'. If this isn't provided, "
            "the system will use 'flatpages/default.html'."
        ),
    )
    registration_required = models.BooleanField(
        _('registration required'),
        help_text=_("If this is checked, only logged-in users will be able to view the page."),
        default=False,
    )
    sites = models.ManyToManyField(Site, verbose_name=_('sites'))

    class Meta:
        app_label = "multilingual_flatpages"
        verbose_name = _('flat page')
        verbose_name_plural = _('flat pages')
        ordering = ('url',)

    def __str__(self):
        return "%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        # Handle script prefix manually because we bypass reverse()
        return iri_to_uri(get_script_prefix().rstrip('/') + self.url)
