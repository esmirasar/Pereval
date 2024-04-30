from django.shortcuts import render
from rest_framework import views, response

from .models import Pereval, User, Coords, Level
from .serializers import (UserSerializer, PerevalSerializer, LevelSerializer,
                          CoordsSerializer, ImagesSerializer)
from django.core.exceptions import ValidationError


class SubmitDataView(views.APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            user = data.pop('user')
            required_user_fields = {'email', 'fam', 'name', 'otc', 'phone'}
            if not all(field in user for field in required_user_fields):
                raise KeyError('user')
            if User.objects.filter(email=user['email']):
                raise ValidationError(message='email')
            user_validator = UserSerializer(data=user)
            user_validator.is_valid(raise_exception=True)
            user_validator.save()

            coords = data.pop('coords')
            required_coords_field = {'latitude', 'longitude', 'height'}
            if not all(field_c in coords for field_c in required_coords_field):
                raise KeyError('coords')
            coords_validator = CoordsSerializer(data=coords)
            coords_validator.is_valid(raise_exception=True)
            coords_validator.save()

            level = data.pop('level')
            required_level_field = {'winter', 'summer', 'autumn', 'spring'}
            if not all(field_l in level for field_l in required_level_field):
                raise KeyError('level')
            level_validator = LevelSerializer(data=level)
            level_validator.is_valid(raise_exception=True)
            level_validator.save()

            pereval = data
            pereval['user'] = User.objects.last().pk
            pereval['coords'] = Coords.objects.last().pk
            pereval['level'] = Level.objects.last().pk
            required_pereval_field = {'beauty_title', 'title', 'other_titles', 'connect', 'add_time'}
            if not all(field_p in pereval for field_p in required_pereval_field):
                raise KeyError('pereval')
            pereval_validator = PerevalSerializer(data=pereval)
            pereval_validator.is_valid(raise_exception=True)
            pereval_validator.save()

            images = data.pop('images')
            for i in images:
                i['pereval'] = Pereval.objects.last().pk
                images_validator = ImagesSerializer(data=i)
                images_validator.is_valid(raise_exception=True)

            for image in images:
                images_validator = ImagesSerializer(data=image)
                images_validator.is_valid(raise_exception=True)
                images_validator.save()

            return response.Response({"status": '200',
                                      "message": 'Отправлено успешно',
                                      "id": Pereval.objects.last().id})
        except KeyError as e:
            return response.Response({
                "status": '400',
                "message": f'Отсутствует одно из обязательных полей: {e.args[0]}',
            })

        except ValidationError as e:
            return response.Response({
                "status": '500',
                "message": f'Ошибка в выполнении операции: {e.message}',
            })
