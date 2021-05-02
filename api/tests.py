from django.urls import reverse

from calendar_event.models import Event
from room.models import ConferenceRoom
from user.models import CalendarUser

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class UserTest(APITestCase):
    def test_create_user(self):
        url = reverse('users-list')
        data = {
            'username': 'username1',
            'email': 'e@mail.com',
            'password': 'asdasddsa'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)


class EventTest(APITestCase):
    def setUp(self):
        self.url = reverse('events-list')
        user_data = {
            'username': 'username2',
            'email': 'e@mail.com',
            'password': 'asdasddsa'
        }
        self.user = CalendarUser.objects.create(**user_data)
        self.token = Token.objects.create(user=self.user)
        location_data = {
            'manager': self.user,
            'name': 'test room',
            'address': 'test street, test city'
        }

        self.location = ConferenceRoom.objects.create(**location_data)

    def test_create_event(self):
        event_data = {
            "name": "test name",
            "agenda": "test agenda",
            "start": "2021-02-09 11:00",
            "end": "2021-02-09 14:00",
            "participants": [self.user.id],
            "location": self.location.id
        }
        response = self.client.post(self.url, event_data, HTTP_AUTHORIZATION=f'Token {self.token}', format='json')
        self.assertEqual(response.status_code, 201)

    def test_event_duration(self):
        event_data = {
            "name": "test name2",
            "agenda": "test agenda2",
            "start": "2021-02-09 01:00",
            "end": "2021-02-09 14:00",
            "participants": [self.user.id],
            "location": self.location.id
        }
        response = self.client.post(self.url, event_data, HTTP_AUTHORIZATION=f'Token {self.token}', format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], ['A meeting cannot last longer than 8 hours.'])

    def test_event_specific_day(self):
        event_data = {
            "name": "test name3",
            "agenda": "test agenda3",
            "start": "2021-02-12 12:00",
            "end": "2021-02-12 14:00",
            "participants": [self.user.id],
            "location": self.location.id
        }
        self.client.post(self.url, event_data, HTTP_AUTHORIZATION=f'Token {self.token}', format='json')
        response = self.client.get(f'{self.url}?day=2021-02-12', HTTP_AUTHORIZATION=f'Token {self.token}', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)

    def test_event_location(self):
        event_data = {
            "name": "test name4",
            "agenda": "test agenda4",
            "start": "2021-04-14 12:00",
            "end": "2021-04-14 14:00",
            "participants": [self.user.id],
            "location": self.location.id
        }
        self.client.post(self.url, event_data, HTTP_AUTHORIZATION=f'Token {self.token}', format='json')
        response = self.client.get(f'{self.url}?location_id={self.location.id}', HTTP_AUTHORIZATION=f'Token {self.token}', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)

    def test_event_by_name_agenda(self):
        event1_data = {
            "name": "regular name",
            "agenda": "super smart plan",
            "start": "2021-04-14 12:00",
            "end": "2021-04-14 14:00",
            "participants": [self.user.id],
            "location": self.location.id
        }
        self.client.post(self.url, event1_data, HTTP_AUTHORIZATION=f'Token {self.token}', format='json')

        event2_data = {
            "name": "super smart name",
            "agenda": "regular plan",
            "start": "2021-05-14 12:00",
            "end": "2021-05-14 14:00",
            "participants": [self.user.id],
            "location": self.location.id
        }
        self.client.post(self.url, event2_data, HTTP_AUTHORIZATION=f'Token {self.token}', format='json')
        response = self.client.get(f'{self.url}?query=smart', HTTP_AUTHORIZATION=f'Token {self.token}', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

    def test_event_owner(self):
        event_data = {
            "name": "test name5",
            "agenda": "test agenda5",
            "start": "2021-04-17 12:00",
            "end": "2021-04-17 14:00",
            "participants": [self.user.id],
            "location": self.location.id
        }
        post_response = self.client.post(self.url, event_data, HTTP_AUTHORIZATION=f'Token {self.token}', format='json')
        self.assertEqual(post_response.status_code, 201)
        event_id = post_response.json()['id']
        response = self.client.get(f'{self.url}{event_id}/', HTTP_AUTHORIZATION=f'Token {self.token}', format='json')
        self.assertEqual(response.json()['owner'], self.user.id)
