from django.contrib.auth import get_user_model
from django.db import models


class Board(models.Model):

    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=True)
    owner = models.ForeignKey(get_user_model(), models.CASCADE, null=False, blank=False)

    def __str__(self):
        return "Board %s: %s" % (self.id, self.name)
