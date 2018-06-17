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

#### Methods to override attributes

**I want to view the user full name in the board API**

#### Detail view
#### Lookup field

### Viewset

#### Default actions
#### Addtl actions - list_route
#### Addtl actions - detail_route

views/api.py
```python
```

urls.py
```python
```

## Serializers

* Add custom RO field
* Custom validation
* Custom serialization / deserialization

## Throttling

## Tests

## Documentation

## Going Further

### View custom logic

* list_route/detail_route
* get_object
* serializer handling, pagination handling

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
