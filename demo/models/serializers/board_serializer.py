from rest_framework import serializers

from demo.models.board import Board


class BoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = ('id', 'name', 'owner_id')
