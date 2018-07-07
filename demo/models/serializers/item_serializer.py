from rest_framework import serializers

from demo.models.item import Item


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('id', 'board', 'title', 'description', 'owner')


class ItemDetailsSerializer(serializers.ModelSerializer):

    board_name = serializers.CharField(source='board.name')
    owner_email = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ('id', 'board_name', 'title', 'description', 'owner_email')

    def get_owner_email(self, obj):
        if obj.owner:
            return obj.owner.email
