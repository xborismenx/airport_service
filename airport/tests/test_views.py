from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase

from airport.models import Airport


class UnauthenticatedViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_airports_unauthorized(self):
        url = reverse("airport:airport-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_routes_unauthorized(self):
        url = reverse("airport:route-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airplane_types_unauthorized(self):
        url = reverse("airport:airplanetype-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airplanes_unauthorized(self):
        url = reverse("airport:airplane-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_orders_unauthorized(self):
        url = reverse("airport:order-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tickets_unauthorized(self):
        url = reverse("airport:ticket-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_flights_unauthorized(self):
        url = reverse("airport:flight-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_crews_unauthorized(self):
        url = reverse("airport:crew-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorizedViewTests(TestCase):
    def setUp(self):
        self.airport = Airport.objects.create()

        self.user = get_user_model().objects.create_user(email="test@mail.com", password="password123", is_staff=True)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_airports_list(self):
        url = reverse("airport:airport-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_airports_detail(self):
        url = reverse("airport:airport-detail", kwargs={"pk": self.airport.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
