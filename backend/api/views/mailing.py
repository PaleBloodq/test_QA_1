import logging
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import *
from .. import serializers, models


__all__ = [
    'Mailing',
]


class Mailing(APIView):
    def patch(self, request: Request):
        serializer = serializers.UpdateMailingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.update(
                models.Mailing.objects.filter(id=serializer.validated_data.get('id')).first(),
                serializer.validated_data
            )
        except AttributeError:
            return Response(status=HTTP_409_CONFLICT)
        except:
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=HTTP_204_NO_CONTENT)
