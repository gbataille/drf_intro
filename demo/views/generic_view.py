from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

from demo.models.board import Board
from demo.models.serializers.board_serializer import BoardSerializer
from demo.models.serializers.user_serializer import UserSerializer


class UserListGenericView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer


class BoardListView(generics.ListAPIView):
    queryset = Board.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    serializer_class = BoardSerializer