import pytest

from notices.models import Notice


@pytest.fixture
def notice():
    yield Notice.objects.create(title="Test title", content="A new thing")
