from django.shortcuts import render
from rest_framework import views, response
from .serializers import (UserSerializer, PerevalSerializer, LevelSerializer,
                          CoordsSerializer, ImagesSerializer)


class SubmitDataView(views.APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        user = data.pop('user')
        user_save = UserSerializer(data=user)
        user_save.is_valid(raise_exception=True)
        user_save.save()
        coords = data.pop('coords')

        level = data.pop('level')
        images = data.pop('images')
        pereval = data
        return response.Response({'request': request.data})
