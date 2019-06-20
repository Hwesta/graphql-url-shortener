from django.db import models


class URLMapping(models.Model):
    """Stores mapping from original URL to shortened URL"""

    # Most web browsers support URLs up to 2000 characters or so
    original_url = models.CharField(
        max_length=2000, help_text="URL to redirect to (max 2000 characters)"
    )
    short_url = models.CharField(
        max_length=20, unique=True, help_text="Short URL string"
    )

    def __str__(self):
        return f"{self.original_url} -> {self.short_url}"
