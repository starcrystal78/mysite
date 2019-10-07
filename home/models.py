from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel


class HomePage(Page):
    max_count = 1
    template = "home/home_page.html"
    banner_title = models.CharField(max_length=120, blank=False, null=True)
    banner_subtitle = RichTextField(features=['bold', 'italic'], blank=True, null=True)
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    banner_cta = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        FieldPanel('banner_title'),
        FieldPanel('banner_subtitle'),
        ImageChooserPanel('banner_image'),
        PageChooserPanel('banner_cta'),

    ]

    class Meta:
        verbose_name = "Home @D Page"
        verbose_name_plural = "Home @D pages"
