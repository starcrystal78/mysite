from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from streams import Blocks


class BlogListingPage(Page):
    """listing page lists all the blog detail pages"""
    template = 'blog/blog_listing_page.html'
    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Overwrites the default title",
    )

    def get_context(self, request, *args, **kwargs):
        """adding custom stuff to our context"""
        context = super().get_context(request, *args, **kwargs)
        context['posts'] = BlogDetailPage.objects.live().public()
        return context

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
    ]


class BlogDetailPage(Page):

    template = 'blog/blog_detail_page.html'
    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Overwrites the default title",
    )

    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )

    content = StreamField(
        [
            ("Full_richtext", Blocks.RichtextBLock()),
            ("simple_richtext", Blocks.SimpleRichtextBLock()),
            ("card", Blocks.CardBlock()),
            ("cta", Blocks.CTABlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        ImageChooserPanel('blog_image'),
        StreamFieldPanel('content'),
    ]


