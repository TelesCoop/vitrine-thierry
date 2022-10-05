from typing import List

from django.db import models
from django import forms
from django.utils.text import slugify

from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    TabbedInterface,
    ObjectList,
    InlinePanel,
)
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from modelcluster.fields import ParentalKey
from model_utils.models import TimeStampedModel


SIMPLE_RICH_TEXT_FIELD_FEATURE = ["bold", "italic", "link", "ol", "ul"]


class Color(models.TextChoices):
    COLOR_BLUE = "gallery-blue", "Bleue"
    COLOR_PURPULE = "gallery-purpule", "Violet"
    COLOR_ORANGE = "gallery-orange", "Orange"
    COLOR_CYAN = "gallery-cyan", "Cyan"
    COLOR_GREEN = "gallery-green", "Vert"
    COLOR_YELLOW = "gallery-yellow", "Jaune"
    COLOR_RED = "gallery-red", "Rouge"


class BannerPage(Page):
    nav_name = models.CharField(
        verbose_name="Nom dans le menu",
        max_length=36,
        default="Accueil",
        help_text="Ce nom d'affichera dans la barre de navigation",
    )

    content_panels = Page.content_panels + [
        FieldPanel("nav_name"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        navbar_banner = BannerSetting.objects.all().first().navbar_banner
        context["banner_url"] = navbar_banner.file.url if navbar_banner else ""
        return context

    class Meta:
        abstract = True


class HomePage(BannerPage):
    # HomePage can be created only on the root
    parent_page_types = ["wagtailcore.Page"]

    artist_name = models.CharField(
        verbose_name="Nom",
        max_length=100,
        null=True,
        blank=True,
        help_text="Si ce champs est vide alors cette partie ne s'affichera pas dans l'Accueil",
    )
    artist_body = RichTextField(
        null=True,
        blank=True,
        verbose_name="Description",
    )
    artist_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    artworks_highlight_title = models.CharField(
        verbose_name="Titre",
        max_length=100,
        null=True,
        blank=True,
        help_text="Si ce champs est vide alors cette partie ne s'affichera pas dans l'Accueil",
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["artworks"] = Artwork.objects.all().filter(
            artworks_highlight__isnull=False
        )
        context["artworks_page"] = ArtworksPage.objects.get()
        return context

    content_panels = BannerPage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("artist_name"),
                FieldPanel("artist_body"),
                FieldPanel("artist_image"),
            ],
            heading="Artiste",
        ),
        MultiFieldPanel(
            [
                FieldPanel("artworks_highlight_title"),
                InlinePanel(
                    "artworks_highlight",
                    label="Oeuvres affichées",
                ),
            ],
            heading="Oeuvres à la une",
        ),
    ]

    # Admin tabs list (Remove promotion and settings tabs)
    edit_handler = TabbedInterface([ObjectList(content_panels, heading="Content")])

    @route("contact/", name="contact")
    def contact(self, request):
        context = self.get_json_list_tags()
        return self.render(
            request, template="home/contact.html", context_overrides=context
        )

    class Meta:
        verbose_name = "Page d'Accueil"


class PresentationPage(RoutablePageMixin, BannerPage):
    parent_page_types = ["HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1

    body = RichTextField(
        null=True,
        blank=True,
        verbose_name="Contenu de la page de présentation",
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = BannerPage.content_panels + [
        FieldPanel("body"),
        FieldPanel("image"),
    ]

    # Admin tabs list (Remove promotion and settings tabs)
    edit_handler = TabbedInterface([ObjectList(content_panels, heading="Content")])

    def save(self, *args, **kwargs):
        self.slug = "qui-suis-je"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Page de presentation"


class WorkExperiencePage(RoutablePageMixin, BannerPage):
    parent_page_types = ["HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1

    body = RichTextField(
        null=True,
        blank=True,
        verbose_name="Introduction de la page parcours",
    )

    parcours_block_data = StreamField(
        [
            (
                "chapters",
                blocks.StructBlock(
                    [
                        ("title", blocks.CharBlock(label="Titre")),
                        (
                            "steps",
                            blocks.ListBlock(
                                blocks.StructBlock(
                                    [
                                        (
                                            "date",
                                            blocks.CharBlock(
                                                label="Date",
                                                required=False,
                                            ),
                                        ),
                                        (
                                            "richtext",
                                            blocks.RichTextBlock(
                                                label="Description",
                                                features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
                                            ),
                                        ),
                                    ],
                                    label_format="{date}",
                                    label="Les différentes étapes de ton parcours",
                                ),
                                label="Etapes",
                            ),
                        ),
                    ],
                    label_format="{title}",
                    label="Parties de ton parcours",
                ),
            )
        ],
        blank=True,
        verbose_name="Parcours",
        use_json_field=True,
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["first_parcours_list_title"] = (
            WorkExperiencePage.objects.all().get().parcours_block_data[0].value["title"]
        )
        return context

    content_panels = BannerPage.content_panels + [
        FieldPanel("body"),
        FieldPanel("parcours_block_data"),
    ]

    # Admin tabs list (Remove promotion and settings tabs)
    edit_handler = TabbedInterface([ObjectList(content_panels, heading="Content")])

    def save(self, *args, **kwargs):
        self.slug = ""
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Page du parcours"


class FreeBodyField(models.Model):
    body = StreamField(
        [
            (
                "heading",
                blocks.CharBlock(form_classname="full title", label="Titre"),
            ),
            (
                "richtext",
                blocks.RichTextBlock(
                    label="Paragraphe",
                ),
            ),
            ("image", ImageChooserBlock(label="Image")),
            ("pdf", DocumentChooserBlock(label="PDF")),
        ],
        blank=True,
        verbose_name="Contenu",
        help_text="Corps de la page",
        use_json_field=True,
    )

    panels = [
        FieldPanel("body", classname="full"),
    ]

    class Meta:
        abstract = True


class ArtworksPage(RoutablePageMixin, BannerPage):
    parent_page_types = ["HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1

    content_panels = BannerPage.content_panels

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["galleries"] = Gallery.objects.all()
        context["artworks"] = Artwork.objects.all()
        return context

    @route(r"^(.*)/$", name="artwork")
    def access_artwork_page(self, request, artwork_slug):
        artwork = Artwork.objects.get(slug=artwork_slug)
        return self.render(
            request,
            context_overrides={
                "artwork": artwork,
                "home_page": HomePage.objects.get(),
                "artworks_page": ArtworksPage.objects.get(),
                "other_news_list": Artwork.objects.exclude(id=artwork.id)[:3],
            },
            template="home/artwork_page.html",
        )

    # Admin tabs list (Remove promotion and settings tabs)
    edit_handler = TabbedInterface([ObjectList(content_panels, heading="Content")])

    def save(self, *args, **kwargs):
        self.slug = "galeries"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Page des galeries"
        verbose_name_plural = "Pages des galeries"


@register_snippet
class Gallery(models.Model):
    name = models.CharField(verbose_name="Nom", max_length=100)
    color = models.CharField(
        max_length=32,
        choices=Color.choices,
        default=Color.COLOR_BLUE,
        help_text="Choisir la couleur de la galerie",
    )

    def __str__(self):
        return self.name

    panels = [
        FieldPanel("name"),
        FieldPanel("color", classname="full"),
    ]

    class Meta:
        verbose_name = "Galerie"


@register_snippet
class Artwork(index.Indexed, TimeStampedModel, FreeBodyField):
    name = models.CharField(verbose_name="Nom de l'oeuvre", max_length=100)
    slug = models.SlugField(
        max_length=100,
        verbose_name="Slug (URL de la ressource)",
        unique=True,
        blank=True,
        default="",
    )
    galleries = models.ManyToManyField(
        Gallery, blank=True, verbose_name="Galeries", related_name="artworks"
    )
    short_description = models.CharField(
        verbose_name="Description courte", max_length=256
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Image principale",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("short_description"),
        FieldPanel("galleries", widget=forms.CheckboxSelectMultiple),
        FieldPanel("image"),
    ] + FreeBodyField.panels

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Oeuvres"
        verbose_name = "Oeuvre"
        ordering = ["-created"]


class HomePageArtworks(models.Model):
    page = ParentalKey(
        HomePage, on_delete=models.CASCADE, related_name="artworks_highlight"
    )
    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.CASCADE,
        verbose_name="Oeuvre",
        related_name="artworks_highlight",
    )

    panels = [
        FieldPanel("artwork"),
    ]

    class Meta:
        unique_together = ("page", "artwork")


class ArticlesPage(RoutablePageMixin, BannerPage):
    parent_page_types = ["HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1

    content_panels = BannerPage.content_panels

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["articles"] = Article.objects.all()
        return context

    @route(r"^(.*)/$", name="article")
    def access_artwork_page(self, request, article_slug):
        article = Article.objects.get(slug=article_slug)
        return self.render(
            request,
            context_overrides={
                "article": article,
                "home_page": HomePage.objects.get(),
                "articles_page": ArticlesPage.objects.get(),
            },
            template="home/article_page.html",
        )

    # Admin tabs list (Remove promotion and settings tabs)
    edit_handler = TabbedInterface([ObjectList(content_panels, heading="Content")])

    def save(self, *args, **kwargs):
        self.slug = "articles"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Page des articles"
        verbose_name_plural = "Pages des articles"


@register_snippet
class ArticleType(models.Model):
    name = models.CharField(
        verbose_name="Nom",
        max_length=100,
        help_text="Exemple: Poème, Extrait de catalogue",
    )

    def __str__(self):
        return self.name

    panels = [
        FieldPanel("name"),
    ]

    class Meta:
        verbose_name = "Type d'article"


@register_snippet
class Article(index.Indexed, TimeStampedModel, FreeBodyField):
    name = models.CharField(verbose_name="Nom de l'article", max_length=100)
    slug = models.SlugField(
        max_length=100,
        verbose_name="Slug (URL de l'article)",
        unique=True,
        blank=True,
        default="",
    )
    types = models.ManyToManyField(
        ArticleType, blank=True, verbose_name="Types d'article", related_name="articles"
    )
    short_description = models.CharField(
        verbose_name="Description courte", max_length=256
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Image principale",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    pdf = models.ForeignKey(
        "wagtaildocs.Document",
        verbose_name="Document principal",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("short_description"),
        FieldPanel("types", widget=forms.CheckboxSelectMultiple),
        FieldPanel("image"),
        FieldPanel("pdf"),
    ] + FreeBodyField.panels

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Articles"
        verbose_name = "Article"
        ordering = ["-created"]


@register_snippet
class FriendlySite(models.Model):
    name = models.CharField(verbose_name="Nom", max_length=100)
    link = models.CharField(verbose_name="Lien", max_length=255)
    display = models.BooleanField(default=True, verbose_name="Afficher")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Sites amis"
        verbose_name = "Site ami"


@register_snippet
class ReferenceSite(models.Model):
    name = models.CharField(verbose_name="Nom", max_length=100)
    link = models.CharField(verbose_name="Lien", max_length=255)
    display = models.BooleanField(default=True, verbose_name="Afficher")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Sites références"
        verbose_name = "Site référence"


@register_setting
class BannerSetting(BaseSetting):
    navbar_banner = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("navbar_banner"),
    ]

    class Meta:
        verbose_name = "Banière-image"
