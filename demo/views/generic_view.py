from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, AllowAny

from demo.models.board import Board
from demo.models.serializers.board_serializer import BoardSerializer
from demo.models.serializers.user_serializer import UserSerializer


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class UserListGenericView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer


class UserRetrieveGenericView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer


class BoardListView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = BoardSerializer
    pagination_class = SmallResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('name',)
    ordering_fields = ('id',)

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(owner=user)
