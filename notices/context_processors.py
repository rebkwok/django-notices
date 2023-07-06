from django.conf import settings
from django.utils.safestring import mark_safe

from notices.models import Notice


def notices(request):
    # first try to load Notice config from settings
    settings_config = Notice.from_settings()
    if settings_config is not None:
        return settings_config

    # if no settings, load latest version from db
    version = Notice.latest_version()
    if version == 0:
        title = content = colour = timeout_seconds = None
    else:
        latest_notice = Notice.latest_notice()
        title = latest_notice.title
        content = latest_notice.content
        safe = getattr(settings, "NOTICES_SAFE", False)
        if safe:
            content = mark_safe(content)
        if hasattr(settings, "NOTICES_COLOUR"):
            colour_setting = "NOTICES_COLOUR"
        else:
            colour_setting = "NOTICES_COLOR"
        colour = getattr(settings, colour_setting, None)
        # cookie timeout; default to 10 years
        timeout_seconds = latest_notice.timeout_seconds
    return {
        "notices_version": version,
        "notices_title": title,
        "notices_content": content,
        "notices_colour": colour,
        "notices_timeout_seconds": timeout_seconds,
    }
