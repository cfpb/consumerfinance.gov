# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel


ENGLISH_PARENT_SLUG = "ask-cfpb"
SPANISH_PARENT_SLUG = "obtener-respuestas"


class NextStep(models.Model):
    title = models.CharField(max_length=255)
    show_title = models.BooleanField(default=False)
    text = RichTextField(blank=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("show_title"),
        FieldPanel("text"),
    ]

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=255)
    name_es = models.CharField(max_length=255)
    slug = models.SlugField(help_text="Do not edit this field")
    slug_es = models.SlugField(help_text="Do not edit this field")
    intro = RichTextField(
        blank=True,
        help_text=(
            "Do not use H2, H3, H4, or H5 to style this text. "
            "Do not add links, images, videos or other rich text elements."
        ),
    )
    intro_es = RichTextField(
        blank=True,
        help_text=(
            "Do not use this field. "
            "It is not currently displayed on the front end."
        ),
    )
    category_image = models.ForeignKey(
        "v1.CFGOVImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=(
            "Select a custom image to appear when visitors share pages "
            "belonging to this category on social media."
        ),
    )
    panels = [
        FieldPanel("name", classname="title"),
        FieldPanel("slug"),
        FieldPanel("intro"),
        FieldPanel("name_es", classname="title"),
        FieldPanel("slug_es"),
        FieldPanel("intro_es"),
        ImageChooserPanel("category_image"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"


class Answer(models.Model):
    last_user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )
    question = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.question

    @property
    def english_page(self):
        return self.answer_pages.filter(language="en").first()

    @property
    def spanish_page(self):
        return self.answer_pages.filter(language="es").first()
