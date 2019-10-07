from django.db import models
# New imports added for ParentalKey, Orderable, InlinePanel, ImageChooserPanel
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
# New imports added for ClusterTaggableManager, TaggedItemBase, MultiFieldPanel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from . import Blocks

class BlogTagIndexPage(Page):
    template = ''
    subtitle = models.CharField(max_length=120, blank=False, null=True)
    content = StreamField(
        [
            ("title_and_text", Blocks.TitleAndTextBlock())
        ]
    )

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        StreamField('content'),
        ]

