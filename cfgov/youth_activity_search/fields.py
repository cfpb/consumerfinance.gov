from modelcluster.fields import ParentalManyToManyField
from mptt.forms import TreeNodeMultipleChoiceField
from mptt.models import TreeManyToManyField


class ParentalTreeManyToManyField(ParentalManyToManyField, TreeManyToManyField):  # noqa: E501
    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', TreeNodeMultipleChoiceField)
        return super(TreeManyToManyField, self).formfield(**kwargs)
