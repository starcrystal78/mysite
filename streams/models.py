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
from . import Blocks


class FlexPage(Page):
    template = 'streams\Flex_page.html'
    content = StreamField(
        [
            ("title_and_text", Blocks.TitleAndTextBlock()),
            ("Full_richtext", Blocks.RichtextBLock()),
            ("simple_richtext", Blocks.SimpleRichtextBLock()),
        ],
        null=True,
        blank=True,
    )
    subtitle = models.CharField(max_length=120, blank=False, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        StreamFieldPanel('content'),
        ]

