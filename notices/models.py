from django.conf import settings
from django.db import models
from django.utils import timezone


class Notice(models.Model):

    title = models.CharField(max_length=255, default="New!")
    content = models.TextField()
    version = models.PositiveIntegerField(blank=True, unique=True)
    starts_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    timeout_seconds = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        starts_str = ""
        if self.starts_at and not self.has_started():
            starts_str = f"starts: {self.starts_at.strftime('%d-%b-%Y %H:%M UTC')} - "
        return (
            f"v{self.version} - {starts_str}"
            f"expires: {self.expires_at.strftime('%d-%b-%Y %H:%M UTC') if self.expires_at else 'never'}"
        )

    @classmethod
    def latest_notice(cls):
        return cls.objects.order_by("-version").first()

    @classmethod
    def latest_version(cls):
        if cls.objects.exists():
            return cls.latest_notice().version
        return 0

    @classmethod
    def from_settings(cls):
        if hasattr(settings, "NOTICES_VERSION"):
            try:
                version = int(settings.NOTICES_VERSION)
            except (TypeError, ValueError):
                ...
            else:
                if hasattr(settings, "NOTICES_COLOUR"):
                    colour_setting = "NOTICES_COLOUR"
                else:
                    colour_setting = "NOTICES_COLOR"

                return {
                    "notices_version": version,
                    "notices_title": getattr(settings, "NOTICES_TITLE", "New!"),
                    "notices_content": getattr(settings, "NOTICES_CONTENT", ""),
                    "notices_colour": getattr(settings, colour_setting, None),
                    "notices_timeout_seconds": getattr(
                        settings, "NOTICES_TIMEOUT_SECONDS", None
                    ),
                }

    def has_expired(self):
        if not self.expires_at:
            return False
        return self.expires_at < timezone.now()

    def has_started(self):
        if not self.starts_at:
            return True
        return self.starts_at < timezone.now()

    def save(self, *args, **kwargs):
        if not self.id and not self.version:
            self.version = Notice.latest_version() + 1
        super().save(*args, **kwargs)
