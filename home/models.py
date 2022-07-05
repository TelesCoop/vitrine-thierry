from typing import List

from django.db import models
from django import forms
from django.utils.text import slugify

from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock

from model_utils.models import TimeStampedModel


SIMPLE_RICH_TEXT_FIELD_FEATURE = ["bold", "italic", "link", "ol", "ul"]


class HomePage(Page):
    # HomePage can be created only on the root
    parent_page_types = ["wagtailcore.Page"]

    body = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name="Introduction du bloc des ressources",
    )

    content_panels = Page.content_panels + [
        FieldPanel("body", classname="full"),
    ]

    class Meta:
        verbose_name = "Page d'Accueil"


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
                    features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
                ),
            ),
            ("image", ImageChooserBlock(label="Image")),
            ("pdf", DocumentChooserBlock(label="PDF")),
        ],
        blank=True,
        verbose_name="Contenu",
        help_text="Corps de la page",
    )

    panels = [
        StreamFieldPanel("body", classname="full"),
    ]

    class Meta:
        abstract = True


@register_snippet
class Gallery(models.Model):
    name = models.CharField(verbose_name="Nom", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Gallerie"


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
        Gallery, blank=True, verbose_name="Galleries", related_name="artworks"
    )
    short_description = models.CharField(
        verbose_name="Description courte", max_length=510
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


class ArtworkPage(Page):
    parent_page_types = ["HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["galleries"] = Gallery.objects.all()
        context["artworks"] = Artwork.objects.all()
        return context

    content_panels = Page.content_panels

    class Meta:
        verbose_name = "Page des galleries"
        verbose_name_plural = "Pages des oeuvres"
