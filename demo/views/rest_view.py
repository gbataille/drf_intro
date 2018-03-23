from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

class ListUsers(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        print("#############")
        print(request.user)
        print("#############")
        usernames = [user.username for user in get_user_model().objects.all()]
        return Response(usernames)
