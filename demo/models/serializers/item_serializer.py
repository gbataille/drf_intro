from rest_framework import serializers

from demo.models.item import Item


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('id', 'board', 'title', 'description', 'owner')
