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
from django import forms
from wagtail.api import APIField
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.core.models import Page, Orderable
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.api.fields import ImageRenditionField
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
    InlinePanel)
from wagtail.snippets.models import register_snippet

from rest_framework.fields import Field
from streams import Blocks


# this class is for aip --== use only for more customization else use ImageRenditionFielda as above
class ImageSerializedField(Field):
    """A custom serializer used in wagtail v2 API"""

    def to_representation(self, value):
        """Returns the image url ,title and dimensions ."""
        return {
            "url": value.file.url,
            "title": value.title,
            "width": value.width,
            "height": value.height,
        }


class BlogAuthorsOrderable(Orderable):
    """This allows us to select one or more blog authors from snippets """

    page = ParentalKey('blog.BlogDetailPage', related_name='blog_authors')
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("author"),
    ]

    # the following property is added so we can see author_name in api ## video 37
    # coding for Everybody / learn Wagtail

    @property
    def author_name(self):
        return self.author.name

    @property
    def author_image(self):
        return self.author.image

    @property
    def author_website(self):
        return self.author.website

    api_fields = [
        APIField('author'),
        APIField("author_name"),
        # APIField("author_image", serializer=ImageSerializedField()),
        APIField("image", serializer=ImageRenditionField('fill-200x250', source="author_image")),
        APIField("author_website"),
    ]


class BlogAuthor(models.Model):
    """Blog author for snippets"""
    name = models.CharField(max_length=120)
    website = models.URLField(blank=True, null=True, )
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
                FieldPanel('website'),
            ],
            heading='links'
        )
    ]

    def __str__(self):
        """String repr of this class"""
        return self.name

    class Meta:
        verbose_name = 'Blog Author'
        verbose_name_plural = 'Blog Authors'


# this is to register the
register_snippet(BlogAuthor)


class BlogCategory(models.Model):
    """Blog category for a snippet"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text="A slug to identify posts by this category"
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = 'Blog Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


register_snippet(BlogCategory)


class BlogListingPage(RoutablePageMixin, Page):
    """listing page lists all the blog detail pages"""
    template = 'blog/blog_listing_page.html'
    max_count = 1
    subpage_types = [
        "blog.ArticleBlogPage",
        "blog.VideoBlogPage",
    ]
    ajax_template = "blog/blog_listing_page_ajax.html"
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
        """Adding custom stuff to our context"""
        context = super().get_context(request, *args, **kwargs)
        # "posts" will have child pages ; you'll need to use .specific in the template
        # in order to access child properties , such as youtube_video_id and subtitle
        all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')
        paginator = Paginator(all_posts, 3)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)

        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts

        # context['Author'] = BlogAuthor.name
        context['category'] = BlogCategory.objects.all()

        return context

    @route(r"july-2019/$", name="july_2019")
    @route(r"^year/(\d+)/(\d+)/$", name= "blog_by_year")
    def blog_by_year(self, request, year=None, month=None):
        context= self.get_context(request)
        return render(request, "blog/latest_posts.html", context)

    @route(r"^category/(?P<cat_slug>[-\w]*)/$", name="category_view")
    def category_view(self, request, cat_slug):
        """Find blog posts based on a category"""
        context = self.get_context(request)
        try:
            category = BlogCategory.objects.get(slug=cat_slug)
        except Exception:
            category = None
        if category is None:
            pass

        context['posts'] = BlogDetailPage.objects.filter(categories__in=[category])

        return render(request, "blog/latest_posts.html", context)

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
            "location": self.full_url + self.reverse_subpage("latest_posts"),
            "lastmod": (self.last_published_at or self.latest_revision_created_at),
            "priority": 0.9,
        })
        return sitemap


class BlogPageTags(TaggedItemBase):
    content_object = ParentalKey(
        'BlogDetailPage',
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


class BlogDetailPage(Page):
    """Parental Blog detail Page"""
    template = 'blog/blog_detail_page.html'
    subpage_type = []
    # limit the page which can be the parent of this page
    parent_page_types = ["blog.BlogListingPage"]

    tags = ClusterTaggableManager(through="BlogPageTags", blank=True)
    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Overwrites the default title",
    )

    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
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
        FieldPanel('tags'),
        ImageChooserPanel('banner_image'),
        StreamFieldPanel('content'),
        MultiFieldPanel([
            InlinePanel("blog_authors", label='Author', min_num=1, max_num=3)
        ],
            heading="Author(s)"
        ),
        MultiFieldPanel([
            FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
        ],
            heading="Categories")
    ]
    # to add the field to the api content url= http://127.0.0.1:8000/api/v2/pages/16/
    api_fields = [
        APIField("blog_authors")
    ]

    def save(self, *args, **kwargs):
        key = make_template_fragment_key(
            "blog_post_preview",
            [self.id]
        )
        cache.delete(key)
        return super().save(*args, **kwargs)


# First subclass blog post page
class ArticleBlogPage(BlogDetailPage):
    """A subclass blog post page for articles"""
    template = "blog/article_blog_page.html"
    subtitle = models.CharField(max_length=120, default='', blank=True, null=True)
    intro_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="best size for this image will be 1400x400"
    )

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        FieldPanel('subtitle'),
        FieldPanel("tags"),
        ImageChooserPanel('banner_image'),
        ImageChooserPanel('intro_image'),
        MultiFieldPanel([
            InlinePanel("blog_authors", label='Author', min_num=1, max_num=3)
        ],
            heading="Author(s)"
        ),
        MultiFieldPanel([
            FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
        ],
            heading="Categories"),
        StreamFieldPanel('content'),
    ]


# second sub class page
class VideoBlogPage(BlogDetailPage):
    template = "blog/video_blog_page.html"
    youtube_video_id = models.CharField(max_length=120)

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        ImageChooserPanel('banner_image'),
        MultiFieldPanel([
            InlinePanel("blog_authors", label='Author', min_num=1, max_num=3)
        ],
            heading="Author(s)"
        ),
        MultiFieldPanel([
            FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
        ],
            heading="Categories"),
        FieldPanel('youtube_video_id'),
        StreamFieldPanel('content'),
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
