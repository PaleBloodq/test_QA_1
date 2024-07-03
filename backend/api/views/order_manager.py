import logging
from django.urls import reverse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *
from api import models
from api.serializers import order_manager as serializers


__all__ = [
    'MyOrders',
]


def check_staff(func):
    def wrapped(self, request: Request, **kwargs):
        if not request.user.is_staff:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                request.get_full_path(),
                reverse('admin:login'),
            )
        return func(self, request, **kwargs)
    return wrapped


class MyOrders(APIView):
    @check_staff
    def get(self, request: Request):
        limit = request.query_params.get('limit', 20)
        offset = request.query_params.get('offset', 0)
        serializer = serializers.OrderSerializer(
            models.Order.objects.filter(
                status=models.Order.StatusChoices.IN_PROGRESS,
                manager=request.user,
            )[offset:limit],
            many=True,
        )
        return Response(serializer.data, status=HTTP_200_OK)


class PaidOrders(APIView):
    @check_staff
    def get(self, request: Request):
        limit = request.query_params.get('limit', 20)
        offset = request.query_params.get('offset', 0)
        serializer = serializers.OrderSerializer(
            models.Order.objects.filter(
                status=models.Order.StatusChoices.PAID,
                manager=None,
            )[offset:limit],
            many=True,
        )
        return Response(serializer.data, status=HTTP_200_OK)


class CompletedOrders(APIView):
    @check_staff
    def get(self, request: Request):
        limit = request.query_params.get('limit', 20)
        offset = request.query_params.get('offset', 0)
        serializer = serializers.OrderSerializer(
            models.Order.objects.filter(
                status=models.Order.StatusChoices.COMPLETED,
            )[offset:limit],
            many=True,
        )
        return Response(serializer.data, status=HTTP_200_OK)


class Order(APIView):
    @check_staff
    def get(self, request: Request):
        limit = request.query_params.get('limit', 20)
        offset = request.query_params.get('offset', 0)
        order_id = request.query_params.get('order_id')
        serializer = serializers.OrderSerializer(
            models.Order.objects.get(id=order_id)
        )
        data = serializer.data
        data['chat'] = serializers.ChatMessageSerializer(
            models.ChatMessage.objects.filter(
                order=serializer.instance
            )[offset:limit],
            many=True,
        ).data
        return Response(data, status=HTTP_200_OK)
