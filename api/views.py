from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ltb.models import LTBType


class FetchNewBook(APIView):
    """
    TODO: Docstring
    """

    @staticmethod
    def _fetch_all_types():
        """
        TODO: Docstring

        :return:
        """
        ltb_types = LTBType.objects.all()
        for ltb_type in ltb_types:
            ltb_type.fetch_next_number()

    def post(self, request, *args, **kwargs):
        """
        TODO: Docstring

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user_name = request.data.get('user')
        password = request.data.get('password')
        user = authenticate(request,
                            username=user_name,
                            password=password)
        if user is not None:
            if user.is_active:
                if user.has_perm('ltb.fetch_new_books'):
                    self._fetch_all_types()
                    message = "Fetch done"
                    http_status = status.HTTP_201_CREATED
                else:
                    message = "No permission"
                    http_status = status.HTTP_403_FORBIDDEN
            else:
                message = "User not active"
                http_status = status.HTTP_403_FORBIDDEN
        else:
            message = "Authentication failed"
            http_status = status.HTTP_403_FORBIDDEN
        return Response(data={"message": message, "user": user_name, "password": password}, status=http_status)
