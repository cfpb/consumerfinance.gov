import re
from decimal import Decimal

from django.core import checks
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


CURRENCY_REGEX = re.compile(r"\$?\d+(\.\d\d)?")


class CurrencyField(models.TextField):
    default_validators = models.TextField.default_validators + [
        RegexValidator(CURRENCY_REGEX)
    ]


class CurrencyDecimalField(models.DecimalField):
    default_validators = models.DecimalField.default_validators + [
        RegexValidator(CURRENCY_REGEX)
    ]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("decimal_places", 2)
        kwargs.setdefault("max_digits", 10)
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, str):
            value = value.lstrip("$")
        elif isinstance(value, float):
            value = Decimal(value).quantize(
                Decimal("1." + "0" * self.decimal_places)
            )

        return super().to_python(value)


class JSONListField(models.JSONField):
    default_error_messages = {"invalid_value": "%(value)s must be a list."}
    description = "A JSON list"
    separator = "; "

    def __init__(self, *args, **kwargs):
        kwargs["default"] = list
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        if not self.choices:
            errors.append(
                checks.Error(
                    "Missing choices.",
                    obj=self,
                    id="tccp.E001",
                )
            )
        return errors

    def validate(self, value, model_instance):
        value = self.ensure_list(value)

        if value:
            if not all(value):
                raise ValidationError(
                    self.error_messages["invalid"],
                    code="invalid",
                    params={"value": value},
                )

            for element in value:
                super().validate(element, model_instance)
        else:
            super().validate(value, model_instance)

    def ensure_list(self, value):
        if not value:
            return self.get_default()

        if isinstance(value, str):
            return value.split(self.separator)

        if value and not isinstance(value, list):
            raise ValueError(value)

        return value

    def get_prep_value(self, value):
        return super().get_prep_value(self.ensure_list(value))

    def get_db_prep_save(self, value, connection):
        return super().get_db_prep_save(self.ensure_list(value), connection)

    def to_python(self, value):
        return super().to_python(self.ensure_list(value))


class YesNoBooleanField(models.BooleanField):
    yes = re.compile("yes", re.IGNORECASE)
    no = re.compile("no", re.IGNORECASE)

    def to_python(self, value):
        if isinstance(value, str):
            if self.yes.match(value):
                return True
            if self.no.match(value):
                return False

        return super().to_python(value)
