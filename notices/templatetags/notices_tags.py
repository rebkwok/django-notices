from classytags.helpers import InclusionTag
from django import template
from django.conf import settings
from django.template.loader import render_to_string

register = template.Library()


class NoticesModal(InclusionTag):
    """
    Displays notices only if user hasn't seen it yet.
    """

    template = "notices/notices.html"

    def render_tag(self, context, **kwargs):
        template_filename = self.get_template(context, **kwargs)
        if "request" not in context:  # pragma: no cover
            return ""

        if settings.NOTICES_VERSION == 0:
            return ""

        try:
            cookie_version = int(context["request"].COOKIES.get("notices_seen"))
        except (ValueError, TypeError):
            cookie_version = 0

        if cookie_version == settings.NOTICES_VERSION:
            return ""

        data = self.get_context(context, **kwargs)
        return render_to_string(
            template_filename, data, getattr(context, "request", None)
        )


register.tag(NoticesModal)
