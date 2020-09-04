from django.contrib.contenttypes.models import ContentType

from model_bakery import baker


# Wagtail's search post_save signal handler attempts to index a page, and uses
# `page.specific()` to ensure it has the specific model instance of the page.
# `specific()` looks that up with the Django ContentType. Model Bakery choses
# a random content type when it creates model instances, and that random
# content type breaks the `specific()` lookup.
#
# This baker is an attempt to get around that problem by ensuring that all our
# bakery model instances ContentType fields default to the ContentType that
# corresponds to their model's.
class ActualContentTypeBaker(baker.Baker):
    """Baker class that uses the real Django ContentType of the model.

    Model Bakery defaults to using a random Django ContentType instance for
    the models it creates instead of a the ContentType that matches the model.

    This baker ensures created ContenType fields default to the ContentType of
    their models.

    This can be overwriten by passing content_type as an explicit value to
    baker.make() or baker.prepare().
    """

    def init_type_mapping(self):
        super().init_type_mapping()
        # Override the `ContentType` mapping to look up the model's actual
        # content type.
        self.type_mapping[ContentType] = lambda: ContentType.objects.get(
            app_label=self.model._meta.app_label,
            model=self.model._meta.model_name
        )
