from datetime import datetime, timezone
import pytest

from notices.models import Notice


pytestmark = pytest.mark.django_db


def test_notice_version_no_notice():
    assert Notice.objects.exists() is False
    assert Notice.latest_version() == 0


def test_notice_version_incremented(notice):
    assert Notice.latest_version() == 1
    Notice.objects.create(title="New Title", content="")
    assert Notice.latest_version() == 2


def test_str(notice):
    assert str(notice) == "v1 - expires: never"


def test_str_with_expiry(notice):
    notice.expires_at = datetime(2022, 12, 1, 10, tzinfo=timezone.utc)
    notice.save()
    assert str(notice) == "v1 - expires: 01-Dec-2022 10:00 UTC"


def test_from_settings_no_notice():
    assert Notice.from_settings() is None


def test_from_settings_with_settings(settings):
    settings.NOTICES_VERSION = 3
    assert Notice.from_settings() == {
        "notices_version": 3,
        "notices_title": "New!",
        "notices_content": "",
        "notices_color": None,
    }


def test_from_settings_with_bad_settings(settings):
    settings.NOTICES_VERSION = "foo"
    assert Notice.from_settings() is None

    settings.NOTICES_VERSION = None
    assert Notice.from_settings() is None
