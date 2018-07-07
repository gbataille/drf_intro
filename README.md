<!-- vim: ts=4 sw=4 et -->

# DRF Presentation

## Setup

* Django app
* User
    * superuser: demo/djangodemo
* Models:
    * Board
    * Item

## Naive approach in django

demo/views/naive.py
```python
from django.http import JsonResponse

from demo.models.board import Board


def naive_view(request):
    boards = Board.objects.all()
    json_payload = {"boards": []}

    for board in boards:
        json_payload['boards'].append({
            'id': board.id,
            'name': board.name,
            'description': board.description,
        })
    return JsonResponse(json_payload, status=200)
```

urls.py
```python
from demo.views import naive

(...)

    url(r'^naive_view/', naive.naive_view),
```

## Using DRF, simple CRUD, model based

### APIViews

Why: Request with addtl methods. Response with content negotiation.

```views/rest_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

class ListUsers(APIView):

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        print("#############")
        print('request.data ~ request.POST + request.FILES')
        print(request.data)
        print('query_params == request.GET')
        print(request.query_params)
        print("#############")
        usernames = [user.username for user in get_user_model().objects.all()]
        return Response(usernames)
```

urls.py
```python
from demo.views.rest_view import ListUsers

(...)

    url(r'^rest/list_users/$', ListUsers.as_view()),
```

Authentication and Permission framework

#### Authentication
settings.py
```python
INSTALLED_APPS = (
    ...
    'rest_framework.authtoken'
)
```
```python
python manage.py migrate
```

views/rest_view.py
```python
from rest_framework import authentication

class ListUsers(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
```

--> Why a tuple? Because methods are tried one after the other until one works
--> Nothing changes?

views/rest_view.py
```python
    def get(self, request, format=None):
        print(request.user)
```

--> We now have a user

#### Permissions

views/rest_view.py
```python
from rest_framework import authentication, permissions

class ListUsers(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
```

--> side effect that I don't like: AnonymousUser is authenticated :(

views/rest_view.py
```python
from rest_framework import authentication, permissions

class ListUsers(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
```

--> normal/djangoregular
--> token
--> 403

### GenericViews

views/generic_view.py
```python
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser


class UserListGenericView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
```

--> Maps to a model through a queryset
--> still exhibits authentication and permissions
--> Built from GenericApiView and mixins

--> 500. Needs to explain how to serialize / deserialize the data

models/serializers/user_serializer.py
```python
from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'email')
```

views/generic_view.py
```python
class UserListGenericView(generics.ListAPIView):
    (...)
    serializer_class = UserSerializer
```

drf_prez/urls.py
```python
    (...)
    url(r'^generic/users/$', UserListGenericView.as_view()),
    (...)
```

**Let's do boards now**

models/serializers/board_serializer.py
```python
from rest_framework import serializers

from demo.models.board import Board


class BoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = ('id', 'name', 'owner_id')
```

views/generic_view.py
```python
class BoardListView(generics.ListAPIView):
    queryset = Board.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    serializer_class = BoardSerializer
```

drf_prez/urls.py
```python
    (...)
    url(r'^generic/boards/$', BoardListView.as_view()),
    (...)
```

**I want to view the user full name in the board API**

models/serializers/board_serializer.py
```python
(...)
class BoardSerializer(serializers.ModelSerializer):
    owner_email = serializers.CharField(source='owner.email')
    owner_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ('id', 'name', 'owner_id', 'owner_email', 'owner_full_name')

    def get_owner_full_name(self, board):
        return "%s %s" % (board.owner.first_name, board.owner.last_name)
```

**I see everybody's board - not cool**


views/generic_view.py
```python
(...)
from rest_framework.permissions import IsAdminUser, AllowAny
(...)

class BoardListView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = BoardSerializer

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(owner=user)
```

#### Pagination

views/generic_view.py
```python
(...)
from rest_framework.pagination import PageNumberPagination
(...)


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000

(...)

class BoardListView(generics.ListAPIView):
    (...)
    pagination_class = SmallResultsSetPagination
    (...)
```

#### Filtering

views/generic_view.py
```python
(...)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

(...)

class BoardListView(generics.ListAPIView):
    (...)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('name',)
    ordering_fields = ('id',)
```

#### Detail view

Now I want to access a specific user. A generic view maps to a single URL.
I need another view/url

views/generic_view.py
```python
class UserRetrieveGenericView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer
```

drf_prez/urls.py
```python
    (...)
    url(r'^generic/users/(?P<id>[0-9]+)/$', UserRetrieveGenericView.as_view()),
    (...)
```

#### Lookup field

views/generic_view.py
```python
class UserRetrieveGenericView(generics.RetrieveAPIView):
    (...)
    lookup_field = 'email'
```

drf_prez/urls.py
```python
    (...)
    url(r'^generic/users/(?P<email>.+)/$', UserRetrieveGenericView.as_view()),
    (...)
```

### Viewset

#### Default actions

models/serializers/item_serializer.py
```python
from rest_framework import serializers

from demo.models.item import Item


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('id', 'board', 'title', 'description', 'owner')
```

views/item_viewset.py
```python
from rest_framework import viewsets

from demo.models.item import Item
from demo.models.serializers.item_serializer import ItemSerializer
from demo.views.generic_view import SmallResultsSetPagination


class ItemViewset(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    pagination_class = SmallResultsSetPagination
    queryset = Item.objects.all()
```

drf_prez/urls.py
```python
    (...)
    from django.conf.urls import include, url
    (...)
    from demo.views.item_viewset import ItemViewset
    (...)


    router = DefaultRouter()
    router.register(r'items', ItemViewset, base_name='item')

    urlpatterns = [
        url(r'^api/', include(router.urls)),
        (...)
    ]
```

#### Limit actions

views/item_viewset.py
```python
    from rest_framework import mixins, viewsets

    (...)
    class ItemViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
    (...)
```

#### Limit visibility

views/item_viewset.py
```python
from django.db import models
from django.contrib.auth.models import AnonymousUser

from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication

(...)
class ItemViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
    serializer_class = ItemSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        qs_filter = models.Q(owner__isnull=True)

        if self.request.user and type(self.request.user) != AnonymousUser:
            qs_filter = qs_filter | models.Q(owner=self.request.user)

        return Item.objects.filter(qs_filter)
```


#### Addtl actions - list_route

views/item_viewset.py
```python
    (...)
    from rest_framework import decorators, response, mixins, viewsets
    (...)

    class ItemViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
        (...)
        @decorators.list_route(methods=['get'])
        def random(self, request):
            import random
            items = list(self.get_queryset())
            idx = random.randint(0, len(items) - 1)

            return response.Response(ItemSerializer(instance=items[idx]).data)
```

#### Addtl actions - detail_route

views/item_viewset.py
```python
    (...)
    from demo.models.serializers.item_serializer import ItemSerializer, ItemDetailsSerializer
    (...)

    class ItemViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
        (...)
        @decorators.detail_route(
            methods=['get'],
            serializer_class=ItemDetailsSerializer
        )
        def with_details(self, request, pk):
            item = self.get_object()
            return response.Response(self.get_serializer_class()(instance=item).data)
```

models/serializers/item_serializer.py
```python
class ItemDetailsSerializer(serializers.ModelSerializer):

    board_name = serializers.CharField(source='board.name')
    owner_email = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ('id', 'board_name', 'title', 'description', 'owner_email')

    def get_owner_email(self, obj):
        if obj.owner:
            return obj.owner.email
```

## Tests

tests.test_views.py
```python
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class SampleTest(APITestCase):

    def test_something(self):
        print(reverse('item-list'))
        print(reverse('item-detail', args=[1]))
        print(reverse('item-random'))
```

tests.test_views.py
```python
    def test_something(self):
        response = self.client.get(
            reverse('item-list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.json())
```

## Documentation

## Serializers

* Add custom RO field
* Custom validation
* Custom serialization / deserialization

## Going Further

### Custom authentication

* Tying to the django user model

### Custom permissions

* Endpoint permission
* Object level permission

### Sub-resources

### Renderers

## Conclusion

* Nice framework, works well
* As usual, great for school cases, but not so simple on real life applications
* Complexity for sub-resources
* Don't like the documentation approach (changing!)
** Only real improvement in the last 2-3 releases
** Reinventing numerous things (openapi vs coreapi)
