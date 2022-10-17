from django.conf import settings


def notices(request):
    return {
        "notices_version": settings.NOTICES_VERSION,
        "notices_title": settings.NOTICES_TITLE,
        "notices_content": settings.NOTICES_CONTENT,
    }
