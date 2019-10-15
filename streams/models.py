from django.db import models
# New imports added for ParentalKey, Orderable, InlinePanel, ImageChooserPanel
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
# New imports added for ClusterTaggableManager, TaggedItemBase, MultiFieldPanel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core import blocks
from . import Blocks



class FlexPage(Page):
    template = 'streams\Flex_page.html'
    subpage_types= ['streams.FlexPage',]
    content = StreamField(
        [
            ("Full_richtext", Blocks.RichtextBLock()),
            ("simple_richtext", Blocks.SimpleRichtextBLock()),
            ("card", Blocks.CardBlock()),
            ("cta", Blocks.CTABlock()),
            ("button_block", Blocks.ButtonBlock()),
            ("Char_block",blocks.CharBlock(
                required=True,
                max_length=255,
                min_length=10,
                help_text='This is help_text'

            ))
        ],
        null=True,
        blank=True,
    )
    ("title_and_text", Blocks.TitleAndTextBlock()),

    subtitle = models.CharField(max_length=120, blank=False, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        StreamFieldPanel('content'),
        ]

