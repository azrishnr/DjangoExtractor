from django.db import models
from datetime import datetime
from django.utils import timezone

class URL(models.Model):
    url_text = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.url_text

    def was_created_recently(self):
        return self.create_at >= timezone.now() - datetime.timedelta(days=1)
