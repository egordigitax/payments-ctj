from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class UserTestCase(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create(email="egordigitax@gmail.com", password="pass", is_staff=True)
        self.assertEqual(user.email, "egordigitax@gmail.com")
        self.assertTrue(user.is_staff)

    def test_client_create_user(self):
        data = {"email": "digitax@mail.ru", "password": "pass"}
        response = self.client.post(reverse("user-list"), data, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_token(self):
        data = {"email": "digitax@mail.ru", "password": "pass"}
        self.client.post(reverse("user-list"), data, content_type='application/json')
        response = self.client.post(reverse("token_obtain_pair"), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        list_res = self.client.get(reverse("user-list"), data, content_type='application/json')
        self.assertEqual(list_res.status_code, 401)

        token = response.data['access']

        headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        list_res2 = self.client.get(reverse("user-list"), **headers)
        self.assertEqual(list_res2.status_code, 200)
