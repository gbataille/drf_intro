from django.contrib import admin

from demo.models.board import Board
from demo.models.item import Item

# Register your models here.

admin.site.register(Board)
admin.site.register(Item)
