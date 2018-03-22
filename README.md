# DRF Presentation

## Setup

* Django app
* User
** superuser: demo/djangodemo
* Models:
** Board
** Item

## Naive approach in django

views.py
```python
def naive_api(self, request):
  return JsonResponse({}, status=200)
```

urls.py
```python
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

## Sub-resources

## Tests

## Documentation
