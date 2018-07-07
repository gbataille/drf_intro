from django.db import models
from django.contrib.auth.models import AnonymousUser

from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication

from demo.models.item import Item
from demo.models.serializers.item_serializer import ItemSerializer


class ItemViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
    serializer_class = ItemSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        qs_filter = models.Q(owner__isnull=True)

        if self.request.user and type(self.request.user) != AnonymousUser:
            qs_filter = qs_filter | models.Q(owner=self.request.user)

        return Item.objects.filter(qs_filter)
