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

    url(r'^rest/list_users/', ListUsers.as_view()),
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

```views/rest_view.py
from rest_framework import authentication

class ListUsers(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
```

--> Why a tuple? Because methods are tried one after the other until one works
--> Nothing changes?

```views/rest_view.py
    def get(self, request, format=None):
        print(request.user)
```

--> We know have a user

#### Permissions

```views/rest_view.py
from rest_framework import authentication, permissions

class ListUsers(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
```

--> side effect that I don't like: AnonymousUser is authenticated :(

```views/rest_view.py
from rest_framework import authentication, permissions

class ListUsers(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
```

--> normal/djangoregular
--> token
--> 403

### APIViews
### APIViews

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

## Filtering

## Pagination

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

## Conclusion

* Nice framework, works well
* As usual, great for school cases, but not so simple on real life applications
* Complexity for sub-resources
* Don't like the documentation approach
** Only real improvement in the last 2-3 releases
** Reinventing numerous things (openapi vs coreapi)
