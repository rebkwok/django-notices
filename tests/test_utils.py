def _assert_contents(response, content_strings, is_in=True):
    content = response.content.decode()
    for content_string in content_strings:
        assert (content_string in content) == is_in


def assert_in_content(response, *content_strings):
    _assert_contents(response, content_strings)


def assert_not_in_content(response, *content_strings):
    _assert_contents(response, content_strings, is_in=False)
