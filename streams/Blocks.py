"""stream fields live here"""
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


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
    cards - blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("Titel", blocks.CharBlock(required=True,  max_length=40)),
                ("Text", blocks.TextBlock(required=True, max_length=200))
            ]
        )
    )



class RichtextBLock (blocks.RichTextBlock):

    class Meta:
        template = "streams/richtext_block.html"
        icon = "doc-full"
        label = 'Full RichText'


class SimpleRichtextBLock (blocks.RichTextBlock):

    def __init__(self, required=True, help_text=None, editor='default', features=None, validators=(), **kwargs):
        super().__init__(**kwargs)
        self.features = [
            "bold",
            "italic",
            'link',
        ]




    class Meta:
        template = "streams/simplerichtext_block.html"
        icon  = "edit"
        label = 'SimpleRichText'
