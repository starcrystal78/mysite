"""stream fields live here"""
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
# from blog.models import BlogDetailPage


class TitleAndTextBlock(blocks.StructBlock):
    """Title and header only"""
    title = blocks.CharBlock(required=True, help_text="Add your Title")
    text = blocks.TextBlock(required=True, help_text="Add additional Text")

    class Meta:
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text "


class CardBlock(blocks.StructBlock):
    """cads with image and text and buttons"""
    title = blocks.CharBlock(required=True, help_text="Add uour title")
    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("name", blocks.CharBlock(required=True, max_length=40)),
                ("text", blocks.TextBlock(required=True, max_length=200)),
                ("button_page", blocks.PageChooserBlock(required=False)),
                ("button_url", blocks.URLBlock(required=False,
                                               help_text="If the button page above is selected, that will be used first"))
            ]
        )
    )

    class Meta:
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "Add cards"


class RichtextBLock(blocks.RichTextBlock):
    class Meta:
        template = "streams/richtext_block.html"
        icon = "doc-full"
        label = 'Full RichText'


class SimpleRichtextBLock(blocks.RichTextBlock):

    def __init__(self, required=True, help_text=None, editor='default', features=None, validators=(), **kwargs):
        super().__init__(**kwargs)
        self.features = [
            "bold",
            "italic",
            'link',
        ]

    class Meta:
        template = "streams/simplerichtext_block.html"
        icon = "edit"
        label = 'SimpleRichText'


class CTABlock(blocks.StructBlock):
    """a simple call to action section """
    title = blocks.CharBlock(required=True)
    text = blocks.RichTextBlock(required=True, features=["bold", "italic", ])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(required=True, default="Learn More", max_length="20")

    class Meta:
        template = "streams/ctablock.html"
        icon = 'edit'
        label = 'CTABlock'


class LinkStructValue(blocks.StructValue):
    """Additional logic for our urls."""
    def url(self):
        button_page = self.get('button_page')
        button_url = self.get('button_url')
        if button_page:
            return button_page.url
        elif button_url:
            return button_url
        return None

    # def latest_post(self):
    #     return BlogDetailPage.objects.live()[:3]


class ButtonBlock(blocks.StructBlock):
    """An external or internal URL """
    button_page = blocks.PageChooserBlock(required=False, help_text='If this is selected the url will be of this page')
    button_url = blocks.URLBlock(required=False, help_text='If page is not selected  this  url will work ')
    #
    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)
    #     context['latest_post'] = BlogDetailPage.objects.live(),public()[:3]

    class Meta:
        template = "streams/button_block.html"
        icon = 'placeholder'
        label = 'call to Action'
        value_class = LinkStructValue
