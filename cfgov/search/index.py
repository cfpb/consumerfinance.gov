from wagtail.search import index


class RelatedFilterField(index.FilterField):
    def __init__(self, field_name, related_field_name, **kwargs):
        super().__init__(field_name, **kwargs)
        self.related_field_name = related_field_name

    def get_attname(self, cls):
        return self.field_name + '__' + self.related_field_name

    def get_value(self, obj):
        return list(
            getattr(obj, self.field_name).values_list(
                self.related_field_name,
                flat=True
            )
        )

    def get_type(self, cls):
        field = self.get_field(cls)
        related_field = field.related_model._meta.get_field(
            self.related_field_name
        )
        return related_field.get_internal_type()
        
