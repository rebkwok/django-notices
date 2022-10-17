import pytest

from http.cookies import SimpleCookie

pytestmark = pytest.mark.django_db


def test_modal(client, settings):
    settings.NOTICES_TITLE = "Test New Notice"
    settings.NOTICES_CONTENT = "Some content\n\nwith multiple lines"
    settings.NOTICES_VERSION = 1

    resp = client.get("/", follow=True)
    assert "Test New Notice" in resp.content.decode()
    assert "<p>Some content</p>\n\n<p>with multiple lines</p>" in resp.content.decode()


def test_version_0(client, settings):
    settings.NOTICES_TITLE = "Test New Notice"
    settings.NOTICES_VERSION = 0

    resp = client.get("/", follow=True)
    assert "Test New Notice" not in resp.content.decode()


def test_version_cookie_seen(client, settings):
    settings.NOTICES_TITLE = "Test New Notice"
    settings.NOTICES_VERSION = 1
    client.cookies = SimpleCookie({"notices_seen": "1"})

    resp = client.get("/", follow=True)
    assert "Test New Notice" not in resp.content.decode()
    settings.NOTICES_VERSION = 2

    resp = client.get("/", follow=True)
    assert "Test New Notice" in resp.content.decode()


def test_unknown_cookie(client, settings):
    settings.NOTICES_TITLE = "Test New Notice"
    settings.NOTICES_VERSION = 1

    # undecipherable cookie, defaults to showing notice
    client.cookies = SimpleCookie({"notices_seen": "unk"})
    resp = client.get("/", follow=True)
    assert "Test New Notice" in resp.content.decode()

    client.cookies = SimpleCookie({"notices_seen": None})
    resp = client.get("/", follow=True)
    assert "Test New Notice" in resp.content.decode()
