from django.db import models

from demo.models.board import Board


class Item(models.Model):

    board = models.ForeignKey(Board, models.CASCADE)
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
