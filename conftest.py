import pytest

from apps.payment_applications.tests.conftest import *  # noqa


def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker(pytest.mark.django_db(databases=['default']))
