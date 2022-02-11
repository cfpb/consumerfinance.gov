import logging
from functools import partial

from django.conf import settings
from django.utils.module_loading import import_string

from requests import Response


logger = logging.getLogger(__name__)


def get_govdelivery_api():
    """Return object that can be used to access the GovDelivery API."""
    clsname = getattr(
        settings,
        'GOVDELIVERY_API',
        'govdelivery.api.GovDelivery'
    )

    cls = import_string(clsname)
    return cls(account_code=settings.GOVDELIVERY_ACCOUNT_CODE)


class MockGovDelivery:
    """Mock class for testing the GovDelivery API.

    Stores all method calls to a list, and returns a valid requests.Response
    object to mimic the behavior of govdelivery.api.GovDelivery.
    """

    calls = []
    """List of calls made to the mock GovDelivery API.

    This list stores all calls made to the mock GovDelivery API, including
    method name and arguments. It is cleared every time a new instance is
    created of MockGovDelivery or one of its descendant classes.

    It lives at the module level to allow for easier use of these mock classes
    in unit tests. When tested code interacts with the GovDelivery API, this
    list can be checked to see what calls were made.

    This is modeled after django.core.mail.outbox.
    """
    def __init__(self, account_code):
        self.account_code = account_code
        MockGovDelivery.calls = []

    def __getattr__(self, name):
        """Route all method calls to the logging function."""
        return partial(self.handle, name)

    def handle(self, method, *args, **kwargs):
        """Log method calls to a list and return a mock response."""
        MockGovDelivery.calls.append((method, args, kwargs))

        response = Response()
        response.status_code = 200
        return response


class ExceptionMockGovDelivery(MockGovDelivery):
    """Mock class for testing the GovDeliveryAPI.

    Behaves like MockGovDelivery but raises a RuntimeError upon invocation of
    any method.
    """
    def handle(self, method, *args, **kwargs):
        super().handle(method, *args, **kwargs)
        raise RuntimeError('test GovDelivery exception')


class ServerErrorMockGovDelivery(MockGovDelivery):
    """Mock class for testing the GovDelivery API.

    Behaves like MockGovDelivery but returns a failing response that contains
    an HTTP status code of 500
    """
    def handle(self, method, *args, **kwargs):
        response = super().handle(
            method,
            *args,
            **kwargs
        )

        response.status_code = 500
        return response


class LoggingMockGovDelivery(MockGovDelivery):
    """Mock class for testing the GovDelivery API.

    Behaves like MockGovDelivery but also logs all method calls.
    """
    def handle(self, method, *args, **kwargs):
        logger.info(
            (
                "GovDelivery(account_code={account_code})."
                "{method}({args}, {kwargs})"
            ).format(
                account_code=self.account_code,
                method=method,
                args=", ".join(map(str, args)),
                kwargs=", ".join(
                    "{k}={v}".format(k=k, v=v) for k, v in kwargs.items()
                )
            )
        )

        return super().handle(
            method,
            *args,
            **kwargs
        )
