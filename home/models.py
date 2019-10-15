from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    PageChooserPanel,
    StreamFieldPanel,
    ObjectList,
    TabbedInterface,

)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.api import APIField
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


class HomePage(RoutablePageMixin, Page):
    max_count = 1
    template = "home/home_page.html"
    # the below subpage is responsible for how many types of page can be created under Home page
    subpage_types = [
        "blog.BlogListingPage",
        "contact.ContactPage",
        "streams.FlexPage",
    ]
    parent_page_types = ["wagtailcore.Page"]
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

# the following line is for adding fields to the api content fields
    api_fields = [
        APIField('banner_title'),
        APIField("banner_subtitle"),
        APIField("banner_image"),
        APIField("banner_cta"),
    ]
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
    banner_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('banner_title'),
            FieldPanel('banner_subtitle'),
            ImageChooserPanel('banner_image'),
            PageChooserPanel('banner_cta'),
        ], heading="banner content"),


    ]
    # To hide the tabs and panel in admin area of home page
    # promote_panels = []
    # settings_panels = []
# this is used for creating the custom tabs in the admin page area of Home
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Custom"),
            ObjectList(Page.promote_panels, heading='Promotional Stuff'),
            ObjectList(Page.settings_panels, heading="Setting Stuff"),
            ObjectList(banner_panels, heading="Banner Setting"),
        ]

    )



    class Meta:
        verbose_name = "Home @D Page"
        verbose_name_plural = "Home @D pages"

    @route(r'^subscribe/$')
    def the_subscribe_page(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        return render(request, "home/subscribe.html", context)


# customize default wagtail page property values
# HomePage._meta.get_field("title").verbose_name = "To any verbose name"
# HomePage._meta.get_field("title").help_text = None
HomePage._meta.get_field("title").default = "Custom Home Page Default"
# HomePage._meta.get_field("slug").default ='home_page_default'