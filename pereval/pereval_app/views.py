from django.shortcuts import render
from rest_framework import views, response

from .models import Pereval, User, Coords, Level, Images
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
            for image in images:
                image['pereval'] = Pereval.objects.last().pk
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


class SubmitDataDetailView(views.APIView):

    def get(self, request, **kwargs):
        pk = kwargs.get('pk')

        if not pk:
            return response.Response({'Ошибка': 'Нет id страницы'})

        instance = Pereval.objects.get(pk=pk)

        instance1 = PerevalSerializer(instance).data
        instance1['user'] = UserSerializer(instance.user).data
        instance1['coords'] = CoordsSerializer(instance.coords).data
        instance1['level'] = LevelSerializer(instance.level).data

        instance_images = Images.objects.filter(pereval=pk)
        instance1['images'] = ImagesSerializer(instance_images, many=True).data

        return response.Response({'Detail': instance1})

    def patch(self, request, *args, **kwargs):

        pk = kwargs.get('pk')

        if not pk:
            return response.Response({'state': 0,
                                      'message': 'Нет id страницы'})

        instance = Pereval.objects.get(pk=pk)

        if not request.data:
            return response.Response({'state': 0,
                                      'message': 'Нет данных для изменений'})

        if instance.status != 'new':
            return response.Response({'state': 0,
                                      'message': 'Запись находится в статусе, при котором изменение недоступно'})

        del request.data['user']
        request_level = request.data.pop('level')
        request_coords = request.data.pop('coords')

        serializer_pereval = PerevalSerializer(data=request.data, instance=instance, partial=True)
        serializer_pereval.is_valid(raise_exception=True)
        serializer_pereval.save()

        instance = Coords.objects.get(pereval=pk)
        serializer_coords = CoordsSerializer(data=request_coords, instance=instance, partial=True)
        serializer_coords.is_valid()
        serializer_coords.save()

        instance = Level.objects.get(pereval=pk)
        serilizer_level = LevelSerializer(data=request_level, instance=instance, partial=True)
        serilizer_level.is_valid()
        serilizer_level.save()

        instance = Images.objects.filter(pereval=pk)
        images = request.data.pop('images')

        if len(instance) < len(images):
            return response.Response(
                {'state': 0,
                 'message': 'Количество введенных данных не должно превышать количество имеющихся фотографий'})

        for i, image in enumerate(images):
            for j, instanc in enumerate(instance):
                if image == instanc:
                    images_validator = ImagesSerializer(data=image, instance=instanc, partial=True)
                    images_validator.is_valid(raise_exception=True)
                    images_validator.save()

        return response.Response({'state': 1,
                                  'message': 'Данные изменены'})
