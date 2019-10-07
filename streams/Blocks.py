"""stream fields live here"""
from wagtail.core import blocks


class TitleAndTextBlock(blocks.StaticBlock):
    """Title and header only"""
    title = blocks.CharBlock(required=True, help_text="Add your Title")
    text = blocks.TextBlock(required=True, help_text="Add additional Text")

    class Meta:
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text "
