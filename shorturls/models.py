import random
import string

from django.db import models

SHORT_URL_CHARACTERS = string.ascii_letters + string.digits
SHORT_URL_LENGTH = 4


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

    @staticmethod
    def generate_short_url():
        """Generate a short URL not in use already"""

        def generate():
            x = "".join(random.choices(SHORT_URL_CHARACTERS, k=SHORT_URL_LENGTH))
            return x

        short_url = generate()
        while URLMapping.objects.filter(short_url=short_url).exists():
            short_url = generate()
        return short_url
