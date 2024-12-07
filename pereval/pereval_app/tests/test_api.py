from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import pdb
from pereval_app.models import User, Coords, Level, Pereval


class PerevalAPITestCase(APITestCase):
    """ тестирование метода get"""

    def test_get(self):
        user = User.objects.create(email="qwewdcdwadcdrty@mail.ru", fam="Пупкин", name="Василий", otc="Иванович",
                                   phone="+75555555", )
        url = reverse('api_view') + '?user__email=qwewdcdwadcdrt@mail.ru'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        url = reverse('api_view') + '?user__email=qwewdcdwadcdrty@mail.ru'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """ тестирование метода post"""

    def test_post(self):
        data = '''{
            "beauty_title": "пер. ",
            "title": "Пхия",
            "other_titles": "Триев",
            "connect": "",
            "user": {
                "email": "qwerty@mail.ru",
                "fam": "Пупкин",
                "name": "Василий",
                "otc": "Иванович",
                "phone": "+7 555 55 55"},
            "coords": {
                "latitude": "45.3842",
                "longitude": "7.1525",
                "height": "1200"},
            "level": {
                "winter": "",
                "summer": "1А",
                "autumn": "1А",
                "spring": ""},
            "images": [{"data": "<картинка1>", "title": "Седловина"}, {"data": "<картинка>", "title": "Подъём"}]
        }'''
        url = reverse('api_view')
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = '''{
            "beauty_title": "пер. ",
            "title": "Пхия",
            "other_titles": "Триев",
            "connect": "",
            "add_time": "bhtjtyjhyt",
            "user": {
                "email": "qwerty@mail.ru",
                "fam": "Пупкин",
                "name": "Василий",
                "otc": "Иванович",
                "phone": "+7 555 55 55"},
            "coords": {
                "latitude": "45.3842",
                "longitude": "7.1525",
                "height": "1200"},
            "level": {
                "winter": "",
                "summer": "1А",
                "autumn": "1А",
                "spring": ""},
            "images": [{"data": "<картинка1>", "title": "Седловина"}, {"data": "<картинка>", "title": "Подъём"}]
        }'''

        url = reverse('api_view')
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class PerevalAPIDetailCase(APITestCase):
    """ тестирование метода get(detail)"""

    def test_get_detail(self):
        user = User.objects.create(email="qwewdcdwadcdrty@mail.ru", fam="Пупкин", name="Василий", otc="Иванович",
                                   phone="+75555555", )
        coords = Coords.objects.create(latitude="45.3842", longitude="7.1525", height="1200")
        level = Level.objects.create(winter="1A", summer="1А", autumn="1А", spring="2B")
        pereval = Pereval.objects.create(beauty_title="пер.", title="Пхия", other_titles="Триев", connect="",
                                         add_time="2021-09-22 13:18:13", user_id=1, coords_id=1, level_id=1)
        url = reverse('api_detail', kwargs={'pk': 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        url = reverse('api_detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_detail(self):
        """ тестироание метода patch"""
        user = User.objects.create(email="qwerty@mail.ru", fam="Пупкин", name="Василий", otc="Иванович",
                                   phone="+75555555", )
        coords = Coords.objects.create(latitude="45.3842", longitude="7.1525", height="1200")
        level = Level.objects.create(winter="1A", summer="1А", autumn="1А", spring="2B")
        pereval = Pereval.objects.create(beauty_title="пер.", title="Пхия", other_titles="Триев", connect="",
                                         add_time="2021-09-22 13:18:13", user_id=user.id, coords_id=coords.id,
                                         level_id=level.id)
        data = """{
          "beauty_title": "перhytjyr. ",
          "title": "Пхия",
          "other_titles": "Триев",
          "connect": "",
          "add_time": "2021-09-22 13:18:13",
          "usergd": {
                "email": "qwerty@mail.ru",
                "fam": "Пупкин",
            "name": "Василий",
            "otc": "Иванович",
                "phone": "+7 555 55 55"},
          "coords":{
              "latitude": "45.3842",
              "longitude": "7.1525",
              "height": "1200"},
          "level":{
                "winter": "",
                "summer": "1А",
                "autumn": "1А",
                "spring": ""}}"""

        url = reverse('api_detail', kwargs={'pk': 2})
        response = self.client.patch(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = """{
          "beauty_title": "перhytjyr. ",
          "title": "Пхия",
          "other_titles": "Триев",
          "connect": "",
          "add_time": "2021-09-22 13:18:13",
          "user": {
                "email": "qwerty@mail.ru",
                "fam": "Пупкин",
            "name": "Василий",
            "otc": "Иванович",
                "phone": "+7 555 55 55"},
          "coords":{
              "latitude": "45.3842",
              "longitude": "7.1525",
              "height": "1200"},
          "level":{
                "winter": "",
                "summer": "1А",
                "autumn": "1А",
                "spring": ""},
          "images": [{"data":"<картинка1>", "title":"Седловина"}, {"data":"<картинка>", "title":"Подъём"}]
}"""
        url = reverse('api_detail', kwargs={'pk': 2})
        response = self.client.patch(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
