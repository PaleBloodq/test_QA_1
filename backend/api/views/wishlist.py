
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *
from api import models, serializers, utils


__all__ = [
    'WishList',
]


class WishList(APIView):
    @utils.auth_required
    def get(self, request: Request, profile: models.Profile):
        return Response(serializers.wishlist_serializer(profile))
    
    @utils.auth_required
    def post(self, request: Request, profile: models.Profile):
        serializer = serializers.ChangeWishListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        models.WishList.follow(profile, serializer.validated_data.get('id'))
        return Response(status=HTTP_204_NO_CONTENT)
    
    @utils.auth_required
    def delete(self, request: Request, profile: models.Profile):
        serializer = serializers.ChangeWishListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        models.WishList.unfollow(profile, serializer.validated_data.get('id'))
        return Response(status=HTTP_204_NO_CONTENT)
