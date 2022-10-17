import pytest

from http.cookies import SimpleCookie

from .test_utils import assert_not_in_content, assert_in_content


pytestmark = pytest.mark.django_db


def test_modal_with_settings(client, settings):
    settings.NOTICES_TITLE = "Test New Notice"
    settings.NOTICES_CONTENT = "Some content\n\nwith multiple lines"
    settings.NOTICES_VERSION = 1

    resp = client.get("/", follow=True)
    assert_in_content(
        resp,
        "Test New Notice",
        "<p>Some content</p>\n\n<p>with multiple lines</p>",
        'id="noticesModal"',
    )


def test_modal_no_settings_or_notices(client, settings):
    resp = client.get("/", follow=True)
    assert resp.status_code == 200
    assert_not_in_content(resp, 'id="noticesClear"', 'id="noticesModal"')


def test_modal_nonsense_settings(client, settings):
    resp = client.get("/", follow=True)
    assert resp.status_code == 200
    settings.NOTICES_VERSION = "foo"
    assert_not_in_content(resp, 'id="noticesClear"', 'id="noticesModal"')


def test_version_0(client, settings):
    settings.NOTICES_TITLE = "Test New Notice"
    settings.NOTICES_VERSION = 0

    resp = client.get("/", follow=True)
    assert_not_in_content(resp, "Test New Notice")
    assert_in_content(resp, 'id="noticesClear"')


def test_version_cookie_seen(client, settings):
    settings.NOTICES_TITLE = "Test New Notice"
    settings.NOTICES_VERSION = 1
    client.cookies = SimpleCookie({"notices_seen": "1"})

    resp = client.get("/", follow=True)
    assert_not_in_content(resp, "Test New Notice")
    settings.NOTICES_VERSION = 2

    resp = client.get("/", follow=True)
    assert_in_content(resp, "Test New Notice")


def test_unknown_cookie(client, settings):
    settings.NOTICES_TITLE = "Test New Notice"
    settings.NOTICES_VERSION = 1

    # undecipherable cookie, defaults to showing notice and clears cookie
    client.cookies = SimpleCookie({"notices_seen": "unk"})
    resp = client.get("/", follow=True)
    assert_in_content(resp, "Test New Notice")

    client.cookies = SimpleCookie({"notices_seen": None})
    resp = client.get("/", follow=True)
    assert_in_content(resp, "Test New Notice")
