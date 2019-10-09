from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel,MultiFieldPanel, InlinePanel, PageChooserPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from streams import Blocks


class HomePageCarouselImage(Orderable):
    """ Between 1 and 5 pages for home page  carousel  """
    page = ParentalKey("home.HomePage", related_name='carousel_image')
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        ImageChooserPanel("carousel_image")
    ]


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

    content = StreamField(
        [
            ("cta", Blocks.CTABlock()),
        ],
        null=True,
        blank=True,
    )
    content_panels = Page.content_panels + [
        MultiFieldPanel([
         FieldPanel('banner_title'),
         FieldPanel('banner_subtitle'),
         ImageChooserPanel('banner_image'),
         PageChooserPanel('banner_cta'),
        ], heading="banner content"),
        MultiFieldPanel([
         InlinePanel("carousel_image", max_num=5, min_num=1, label="Image"),
        ], heading='carousel Image'),
        FieldPanel('body', classname="full"),
        StreamFieldPanel('content'),

    ]

    class Meta:
        verbose_name = "Home @D Page"
        verbose_name_plural = "Home @D pages"
