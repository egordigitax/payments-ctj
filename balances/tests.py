from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class BalancesTestCase(TestCase):

    def test_balance_list(self):
        data = {"email": "digitax@mail.ru"}
        self.client.post(reverse("user-list"), data, content_type='application/json')
        response = self.client.post(reverse("token_obtain_pair"), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        list_res = self.client.get(reverse("user-list"), data, content_type='application/json')
        self.assertEqual(list_res.status_code, 401)

        token = response.data['access']

        headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        list_res2 = self.client.get(reverse("user-list"), **headers)
        self.assertEqual(list_res2.status_code, 200)

        list_balances = self.client.get(reverse("balance-list"), **headers)
        self.assertEqual(list_balances.status_code, 200)

        data = {"type": "DP", "amount": "500"}
        make_transaction = self.client.post(reverse("transaction-list"), data=data, content_type='application/json',
                                            **headers)
        self.assertEqual(make_transaction.status_code, 201)

        data = {"type": "DP", "amount": ""}
        make_transaction2 = self.client.post(reverse("transaction-list"), data=data, content_type='application/json',
                                             **headers)
        self.assertEqual(make_transaction2.status_code, 400)

        make_transaction3 = self.client.get(reverse("balance-list"), **headers)
        self.assertEqual(make_transaction3.json()['balance'], '500.00')

        data = {"type": "DP", "amount": "250"}
        make_transaction = self.client.post(reverse("transaction-list"), data=data, content_type='application/json',
                                            **headers)
        self.assertEqual(make_transaction.status_code, 201)

        make_transaction3 = self.client.get(reverse("balance-list"), **headers)
        self.assertEqual(make_transaction3.json()['balance'], '750.00')

        data = {"type": "WD", "amount": "100"}
        make_transaction = self.client.post(reverse("transaction-list"), data=data, content_type='application/json',
                                            **headers)
        self.assertEqual(make_transaction.status_code, 201)

        make_transaction3 = self.client.get(reverse("balance-list"), **headers)
        self.assertEqual(make_transaction3.json()['balance'], '650.00')

        data = {"type": "WD", "amount": "100000"}
        make_transaction = self.client.post(reverse("transaction-list"), data=data, content_type='application/json',
                                            **headers)
        self.assertEqual(make_transaction.status_code, 402)