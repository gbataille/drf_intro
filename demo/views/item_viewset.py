from rest_framework import viewsets

from demo.models.item import Item
from demo.models.serializers.item_serializer import ItemSerializer


class ItemViewset(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
