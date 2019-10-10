
# ###################### The old blog model import files #########################
# from django.db import models
# # New imports added for ParentalKey, Orderable, InlinePanel, ImageChooserPanel
# from modelcluster.fields import ParentalKey
# from wagtail.core.models import Page, Orderable
# from wagtail.core.fields import RichTextField
# from wagtail.images.edit_handlers import ImageChooserPanel
# from wagtail.search import index
# # New imports added for ClusterTaggableManager, TaggedItemBase, MultiFieldPanel
# from modelcluster.contrib.taggit import ClusterTaggableManager
# from taggit.models import TaggedItemBase
# from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel

# ############old model import ends

from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
    InlinePanel)
from wagtail.snippets.models import register_snippet

from streams import Blocks


class BlogAuthorsOrderable(Orderable):
    """This allows us to select one or more blog authors from snippets """

    page = ParentalKey('blog.BlogDetailPage', related_name='blog_authors')
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("author")
    ]


class BlogAuthor(models.Model):
    """Blog author for snippets"""
    name = models.CharField(max_length=120)
    website = models.URLField(blank=True, null=True,)
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                ImageChooserPanel("image"),
            ],
            heading="Name and Image",
        ),
        MultiFieldPanel(
            [
                FieldPanel('website')
            ],
            heading='links'
        )
    ]

    def __str__(self):
        """String rep of this class"""
        return self.name

    class Meta:
        verbose_name = 'Blog Author'
        verbose_name_plural = 'Blog Authors'


# this is to register the
register_snippet(BlogAuthor)


class BlogListingPage(RoutablePageMixin, Page):
    """listing page lists all the blog detail pages"""
    template = 'blog/blog_listing_page.html'
    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Overwrites the default title",
    )
    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
    ]

    def get_context(self, request, *args, **kwargs):
        """adding custom stuff to our context"""
        context = super().get_context(request, *args, **kwargs)
        context['posts'] = BlogDetailPage.objects.live().public()
        context[BlogAuthor] = BlogAuthor.objects.all()
        return context

    @route(r'^latest/$', name='latest_posts')
    def latest_blog_posts(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context['latest_posts'] = BlogDetailPage.objects.live().public()[:2]
        return render(request, "blog/latest_posts.html", context)

    def get_sitemap_urls(self, request):
        # uncomment the following line to have no sitemap of this page
        # return []
        sitemap = super().get_sitemap_urls(request)
        sitemap.append({
            "location": self.full_url+ self.reverse_subpage("latest_posts"),
            "lastmod": (self.last_published_at or self.latest_revision_created_at),
            "priority": 0.9,
        })
        return sitemap


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
        MultiFieldPanel([
            InlinePanel("blog_authors", label='Author', min_num=1, max_num=3)
        ],
        heading="Author(s)"
        )
    ]

# ############################ the OLd blog models.py content here #############################################

#
#
# class BlogIndexPage(Page):
#     intro = RichTextField(blank=True)
#
#     content_panels = Page.content_panels + [
#         FieldPanel('intro', classname="full")
#     ]
#
#
# class BlogPageTag(TaggedItemBase):
#     content_object = ParentalKey(
#         'BlogPage',
#         related_name='tagged_items',
#         on_delete=models.CASCADE
#     )
#
#
# class BlogPage(Page):
#     date = models.DateField("Post date")
#     intro = models.CharField(max_length=250)
#     body = RichTextField(blank=True)
#     tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
#
#     def main_image(self):
#         gallery_item = self.gallery_images.first()
#         if gallery_item:
#             return gallery_item.image
#         else:
#             return None
#
#     search_fields = Page.search_fields + [
#         index.SearchField('intro'),
#         index.SearchField('body'),
#     ]
#
#     content_panels = Page.content_panels + [
#         MultiFieldPanel([
#             FieldPanel('date'),
#             FieldPanel('tags'),
#         ], heading="Blog information"),
#         FieldPanel('intro'),
#         FieldPanel('body'),
#         InlinePanel('gallery_images', label="Gallery images"),
#     ]
#
#
# class BlogPageGalleryImage(Orderable):
#     page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
#     image = models.ForeignKey(
#         'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
#     )
#     caption = models.CharField(blank=True, max_length=250)
#
#     panels = [
#         ImageChooserPanel('image'),
#         FieldPanel('caption'),
#     ]
#
#
# class BlogTagIndexPage(Page):
#
#     def get_context(self, request):
#
#         # Filter by tag
#         tag = request.GET.get('tag')
#         blogpages = BlogPage.objects.filter(tags__name=tag)
#
#         # Update template context
#         context = super().get_context(request)
#         context['blogpages'] = blogpages
#         return context
