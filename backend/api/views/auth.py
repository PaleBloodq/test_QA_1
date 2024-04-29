from datetime import datetime, date
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Sum
from api import models, serializers, utils


class GetToken(APIView):
    def post(self, request: Request):
        telegram_id = request.data.get('telegram_id')
        if telegram_id:
            return Response({
                'token': utils.encode_profile(telegram_id)
            }, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RefreshToken(APIView):
    def post(self, request: Request):
        token = request.data.get('token')
        if token:
            profile = utils.decode_token(token)
            if profile:
                return Response({
                    'token': utils.encode_profile(profile.telegram_id)
                }, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class VerifyToken(APIView):
    def post(self, request: Request):
        token = request.data.get('token')
        if token:
            if utils.decode_token(token):
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class Profile(APIView):
    @utils.auth_required
    def get(self, request: Request, profile: models.Profile):
        response = serializers.ProfileSerializer(profile).data
        return Response(response)


class UpdateProfile(APIView):
    @utils.auth_required
    def post(self, request: Request, profile: models.Profile):
        if request.data.get('psEmail'):
            profile.playstation_email = request.data.get('psEmail')
        if request.data.get('psPassword'):
            profile.playstation_password = request.data.get('psPassword')
        if request.data.get('billEmail'):
            profile.bill_email = request.data.get('billEmail')
        try:
            profile.save()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        response = serializers.ProfileSerializer(profile).data
        return Response(response)