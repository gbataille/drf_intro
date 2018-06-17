from rest_framework import serializers

from demo.models.board import Board


class BoardSerializer(serializers.ModelSerializer):
    owner_email = serializers.CharField(source='owner.email')
    owner_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ('id', 'name', 'owner_id', 'owner_email', 'owner_full_name')

    def get_owner_full_name(self, board):
        return "%s %s" % (board.owner.first_name, board.owner.last_name)
