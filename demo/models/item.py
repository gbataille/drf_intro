from django.contrib.auth import get_user_model
from django.db import models

from demo.models.board import Board


class Item(models.Model):

    board = models.ForeignKey(Board, models.CASCADE)
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(get_user_model(), models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "Item %s: %s" % (self.id, self.title)
