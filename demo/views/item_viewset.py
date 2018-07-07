from django.db import models
from django.contrib.auth.models import AnonymousUser

from rest_framework import decorators, response, mixins, viewsets
from rest_framework.authentication import TokenAuthentication

from demo.models.item import Item
from demo.models.serializers.item_serializer import ItemSerializer, ItemDetailsSerializer
from demo.views.generic_view import SmallResultsSetPagination


class ItemViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
    serializer_class = ItemSerializer
    authentication_classes = (TokenAuthentication,)
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        qs_filter = models.Q(owner__isnull=True)

        if self.request.user and type(self.request.user) != AnonymousUser:
            qs_filter = qs_filter | models.Q(owner=self.request.user)

        return Item.objects.filter(qs_filter)

    @decorators.list_route(methods=['get'])
    def random(self, request):
        import random
        items = list(self.get_queryset())
        idx = random.randint(0, len(items) - 1)

        return response.Response(ItemSerializer(instance=items[idx]).data)

    @decorators.detail_route(
        methods=['get'],
        serializer_class=ItemDetailsSerializer
    )
    def with_details(self, request, pk):
        item = self.get_object()
        return response.Response(self.get_serializer_class()(instance=item).data)
