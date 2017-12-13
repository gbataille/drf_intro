from django.db import models


class Board(models.Model):

    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=True)
