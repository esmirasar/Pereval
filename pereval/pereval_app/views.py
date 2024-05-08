from django.shortcuts import render
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiRequest, OpenApiResponse, OpenApiExample
from rest_framework import views, response, status

from .models import Pereval, User, Coords, Level, Images
from .serializers import (UserSerializer, PerevalSerializer, LevelSerializer,
                          CoordsSerializer, ImagesSerializer)
from django.core.exceptions import ValidationError


class SubmitDataView(views.APIView):
    """ метод get для вывода записей, отправленных с user__email"""

    @extend_schema(
        parameters=[OpenApiParameter(name='user__email',
                                     description='Введите email',
                                     type=OpenApiTypes.EMAIL)],
        description='Поиск по email',
        responses=OpenApiResponse(response=PerevalSerializer,
                                  description='Вывод обхекта перевала по email',
                                  examples=[OpenApiExample(name='Детали',
                                                           value={'id': 'Идентификатор объекта',
                                                                  'beauty_title': 'Основное название',
                                                                  'title': 'Название',
                                                                  'other_title': 'Альтернативное название',
                                                                  'connect': 'То что соединяет перевал',
                                                                  'add_time': 'Время добавления',
                                                                  'user': 'Автор',
                                                                  'coords': 'Координаты перевала',
                                                                  'level': 'Уровень прохождения (2 символа)',
                                                                  'images': 'Список добавленных фотографий',
                                                                  'status': 'Статус модерации'
                                                                  }),
                                            OpenApiExample(name='Типы данных',
                                                           value={'id': 'integer',
                                                                  'beauty_title': 'string',
                                                                  'title': 'string',
                                                                  'other_title': 'Аstring',
                                                                  'connect': 'string',
                                                                  'add_time': 'datetime',
                                                                  'user': {'email': 'string email',
                                                                           'fam': 'string',
                                                                           'name': 'string',
                                                                           'otc': 'string',
                                                                           'phone': 'string'},
                                                                  'coords': {'latitude': 'float',
                                                                             'longitude': 'float',
                                                                             'height': 'integer'},
                                                                  'level': {'winter': 'string 2 symbol',
                                                                            'summer': 'string 2 symbol',
                                                                            'autumn': 'string 2 symbol',
                                                                            'spring': 'string 2 symbol'},
                                                                  'images': [{'data': 'File (image)',
                                                                              'title': 'string'}
                                                                  ]}

                                                           )
                                            ]
                                  )
    )

    def get(self, request):
        try:
            instance = User.objects.get(email=request.GET['user__email'])
        except:
            return response.Response({'Ошибка': 'Строка email'}, status=status.HTTP_400_BAD_REQUEST)
        instance_user = User.objects.filter().values('email')
        pk = instance.id
        list_pereval = Pereval.objects.filter(user_id=pk)
        serializer_per = PerevalSerializer(list_pereval, many=True).data
        return response.Response({'Список': serializer_per}, status=status.HTTP_200_OK)

    """метод post для отправки записи"""

    @extend_schema(description='Добавление нового щбъекта перевала',
                   request={'multipart/form-data': {'type': 'object',
                                                    'properties': {'beauty_title': {'type': 'string'},
                                                                   'title': {'type': 'string'},
                                                                   'other_titles': {'type': 'string'},
                                                                   'connect': {'type': 'string'},
                                                                   'add_time': {'type': 'string',
                                                                                'format': 'date-time'},
                                                                   'user': {'type': 'object',
                                                                            'format': 'byte',
                                                                            'properties': {'email': {'type': 'string',
                                                                                                     'format': 'email'},
                                                                                           'fam': {'type': 'string'},
                                                                                           'name': {'type': 'string'},
                                                                                           'otc': {'type': 'string'},
                                                                                           'phone': {'type': 'string'}
                                                                                           }
                                                                            },
                                                                   'coords': {'type': 'object',
                                                                              'format': 'byte',
                                                                              'properties': {
                                                                                  'latitude': {'type': 'number',
                                                                                               'format': 'float'},
                                                                                  'longitude': {'type': 'number',
                                                                                                'format': 'float'},
                                                                                  'height': {'type': 'integer'}
                                                                                  }
                                                                              },
                                                                   'level': {'type': 'object',
                                                                             'format': 'byte',
                                                                             'properties': {
                                                                                 'winter': {'type': 'string'},
                                                                                 'summer': {'type': 'string'},
                                                                                 'autumn': {'type': 'string'},
                                                                                 'spring': {'type': 'string'}
                                                                                 }
                                                                             },
                                                                   'image': {'type': 'string',
                                                                             'format': 'binary'},
                                                                   'title_image': {'type': 'string'}}}},
                   responses=OpenApiResponse(response=PerevalSerializer,
                                             description='Вывод данных',
                                             examples=[OpenApiExample(name='return 200',
                                                                      value={'status': 200,
                                                                             'message': 'Данные сохранены',
                                                                             'id': 'Номер добавленного объекта'},
                                                                      description='Успешное выполнение запроса'),
                                                       OpenApiExample(name='return 400',
                                                                      value={'status': 400,
                                                                             'message': 'Ошибка в названии поля',
                                                                             'id': None},
                                                                      description='В случае ошибки в названии поля'),
                                                       OpenApiExample(name='return 500',
                                                                      value={'status': 500,
                                                                             'message': 'Данные не сохранены. Ошибка:',
                                                                             'id': None},
                                                                      description='В случае какой-либо ошибки')]))
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            user = data.pop('user')
            required_user_fields = {'email', 'fam', 'name', 'otc', 'phone'}
            if not all(field in user for field in required_user_fields):
                raise KeyError('user')
            if User.objects.filter(email=user['email']):
                user = User.objects.get(email=user['email']).pk
            else:
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
            if type(user) is dict:
                pereval['user'] = User.objects.last().pk
            else:
                pereval['user'] = user
            pereval['coords'] = Coords.objects.last().pk
            pereval['level'] = Level.objects.last().pk
            required_pereval_field = {'beauty_title', 'title', 'other_titles', 'connect', 'add_time'}
            if not all(field_p in pereval for field_p in required_pereval_field):
                raise KeyError('pereval')
            pereval_validator = PerevalSerializer(data=pereval)
            pereval_validator.is_valid()
            pereval_validator.save()

            images = data.pop('images')
            for image in images:
                image['pereval'] = Pereval.objects.last().pk
                images_validator = ImagesSerializer(data=image)
                images_validator.is_valid(raise_exception=True)
                images_validator.save()

            return response.Response({"status": '200',
                                      "message": 'Отправлено успешно',
                                      "id": Pereval.objects.last().id}, status=status.HTTP_200_OK)
        except KeyError as e:
            return response.Response({
                "status": '400',
                "message": f'Отсутствует одно из обязательных полей: {e.args[0]}',
            }, status=status.HTTP_400_BAD_REQUEST)

        except AssertionError as e:
            return response.Response({
                "status": '500',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubmitDataDetailView(views.APIView):

    """метод get для вывода детальной информации"""

    @extend_schema(
        parameters=[OpenApiParameter(name='user__email',
                                     description='Введите email',
                                     type=OpenApiTypes.EMAIL)],
        description='Поиск по email',
        responses=OpenApiResponse(response=PerevalSerializer,
                                  description='Вывод обхекта перевала по его id',
                                  examples=[OpenApiExample(name='Детали',
                                                           value={'id': 'Идентификатор объекта',
                                                                  'beauty_title': 'Основное название',
                                                                  'title': 'Название',
                                                                  'other_title': 'Альтернативное название',
                                                                  'connect': 'То что соединяет перевал',
                                                                  'add_time': 'Время добавления',
                                                                  'user': 'Автор',
                                                                  'coords': 'Координаты перевала',
                                                                  'level': 'Уровень прохождения (2 символа)',
                                                                  'images': 'Список добавленных фотографий',
                                                                  'status': 'Статус модерации'
                                                                  }),
                                            OpenApiExample(name='Типы данных',
                                                           value={'id': 'integer',
                                                                  'beauty_title': 'string',
                                                                  'title': 'string',
                                                                  'other_title': 'Аstring',
                                                                  'connect': 'string',
                                                                  'add_time': 'datetime',
                                                                  'user': {'email': 'string email',
                                                                           'fam': 'string',
                                                                           'name': 'string',
                                                                           'otc': 'string',
                                                                           'phone': 'string'},
                                                                  'coords': {'latitude': 'float',
                                                                             'longitude': 'float',
                                                                             'height': 'integer'},
                                                                  'level': {'winter': 'string 2 symbol',
                                                                            'summer': 'string 2 symbol',
                                                                            'autumn': 'string 2 symbol',
                                                                            'spring': 'string 2 symbol'},
                                                                  'images': [{'data': 'File (image)',
                                                                              'title': 'string'}]
                                                                  }
                                                           )
                                            ]
                                  )
    )
    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        try:
            instance = Pereval.objects.get(pk=pk)
        except:
            return response.Response({'Ошибка': 'Нет id страницы'}, status=status.HTTP_400_BAD_REQUEST)

        instance1 = PerevalSerializer(instance).data
        instance1['user'] = UserSerializer(instance.user).data
        instance1['coords'] = CoordsSerializer(instance.coords).data
        instance1['level'] = LevelSerializer(instance.level).data

        instance_images = Images.objects.filter(pereval=pk)
        instance1['images'] = ImagesSerializer(instance_images, many=True).data

        return response.Response({'Detail': instance1}, status=status.HTTP_200_OK)

    """метод patch для изменения записи"""

    @extend_schema(description='Изменение перевала по его уникальному номеру',
                   request={'multipart/form-data': {'type': 'object',
                                                    'properties': {'beauty_title': {'type': 'string'},
                                                                   'title': {'type': 'string'},
                                                                   'other_titles': {'type': 'string'},
                                                                   'connect': {'type': 'string'},
                                                                   'add_time': {'type': 'string',
                                                                                'format': 'date-time'},
                                                                   'coords': {'type': 'object',
                                                                              'format': 'byte',
                                                                              'properties': {
                                                                                  'latitude': {'type': 'number',
                                                                                               'format': 'float'},
                                                                                  'longitude': {'type': 'number',
                                                                                                'format': 'float'},
                                                                                  'height': {'type': 'integer'}
                                                                                  }
                                                                              },
                                                                   'level': {'type': 'object',
                                                                             'format': 'byte',
                                                                             'properties': {
                                                                                 'winter': {'type': 'string'},
                                                                                 'summer': {'type': 'string'},
                                                                                 'autumn': {'type': 'string'},
                                                                                 'spring': {'type': 'string'}
                                                                                 }
                                                                             },
                                                                   'data': {'type': 'string',
                                                                            'format': 'binary'},
                                                                   'image_title': {'type': 'string'}
                                                                   }
                                                    }
                            },
                   responses=OpenApiResponse(response=PerevalSerializer,
                                             description='Изменение перевела',
                                             examples=[OpenApiExample(name='Детали',
                                                                      value={'id': 'Идентификатор объекта',
                                                                             'status': 'Статус модерации',
                                                                             'beauty_title': 'Основное название',
                                                                             'title': 'Название',
                                                                             'other_title': 'Альтернативное название',
                                                                             'connect': 'То что соединяет перевал',
                                                                             'add_time': 'Время добавления',
                                                                             'user': 'Автор',
                                                                             'coords': 'Координаты перевала',
                                                                             'level': 'Уровень прохождения (2 символа)',
                                                                             'images': 'Список добавленных фотографий'}
                                                                      ),
                                                       OpenApiExample(name='Вывод типов данных',
                                                                      value={'id': 'integer',
                                                                             'status': 'string',
                                                                             'beauty_title': 'string',
                                                                             'title': 'string',
                                                                             'other_title': 'string',
                                                                             'connect': 'string',
                                                                             'add_time': 'datetime',
                                                                             'user': {'email': 'string email',
                                                                                      'fam': 'string',
                                                                                      'name': 'string',
                                                                                      'otc': 'string',
                                                                                      'phone': 'string'},
                                                                             'coords': {'latitude': 'float',
                                                                                        'longitude': 'float',
                                                                                        'height': 'integer'},
                                                                             'level': {'winter': 'string 2 symbol',
                                                                                       'summer': 'string 2 symbol',
                                                                                       'autumn': 'string 2 symbol',
                                                                                       'spring': 'string 2 symbol'},
                                                                             'images': [{'data': 'File (image)',
                                                                                         'title': 'string'}]
                                                                             }
                                                                      )
                                                       ]
                                             )
                   )
    def patch(self, request, *args, **kwargs):

        pk = kwargs.get('pk')

        try:
            instance = Pereval.objects.get(pk=pk)
        except:
            return response.Response({'state': 0,
                                      'message': 'Нет id страницы'}, status=status.HTTP_400_BAD_REQUEST)

        if not request.data:
            return response.Response({'state': 0,
                                      'message': 'Нет данных для изменений'}, status=status.HTTP_400_BAD_REQUEST)

        if instance.status != 'new':
            return response.Response({'state': 0,
                                      'message': 'Запись находится в статусе, при котором изменение недоступно'},
                                     status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('user'):
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
        if request.data.get('images'):
            images = request.data.pop('images')

            if len(instance) < len(images):
                return response.Response(
                    {'state': 0,
                     'message': 'Количество введенных данных не должно превышать количество имеющихся фотографий'},
                    status=status.HTTP_400_BAD_REQUEST)

            for i, image in enumerate(images):
                for j, instanc in enumerate(instance):
                    if image == instanc:
                        images_validator = ImagesSerializer(data=image, instance=instanc, partial=True)
                        images_validator.is_valid(raise_exception=True)
                        images_validator.save()

        return response.Response({'state': 1,
                                  'message': 'Данные изменены'}, status=status.HTTP_200_OK)
