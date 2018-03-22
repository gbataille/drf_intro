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

## Authentication

* Tying to the django user model

## Permissions

* Endpoint permission
* Object level permission

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

### Sub-resources

## Conclusion

* Nice framework, works well
* As usual, great for school cases, but not so simple on real life applications
* Complexity for sub-resources
* Don't like the documentation approach
** Only real improvement in the last 2-3 releases
** Reinventing numerous things (openapi vs coreapi)
