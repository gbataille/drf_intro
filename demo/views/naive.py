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
