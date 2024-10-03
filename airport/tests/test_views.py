from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase

from airport.models import Airport, Route, AirplaneType, Airplane, Order, Flight, Ticket, Crew


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
        self.airport_1 = Airport.objects.create(name="Milan national airport", closest_big_city="Milan")
        self.airport_2 = Airport.objects.create(name="Paris Charles de Gaulle", closest_big_city="Paris")
        self.route = Route.objects.create(source=self.airport_1, destination=self.airport_2, distance=850)
        self.airplane_type = AirplaneType.objects.create(name="Boeing 737")
        self.airplane = Airplane.objects.create(name="Airplane 1", rows=6, seats_in_row=10,
                                                airplane_type=self.airplane_type)

        self.user = get_user_model().objects.create_user(email="test@mail.com", password="password123", is_staff=True)
        self.order = Order.objects.create(user=self.user)
        self.flight = Flight.objects.create(route=self.route, airplane=self.airplane,
                                            departure_time="2024-10-10T08:00:00Z",
                                            arrival_time="2024-10-10T10:00:00Z")
        self.crew = Crew.objects.create()
        self.crew.flight.add(self.flight)
        self.ticket = Ticket.objects.create(flight=self.flight, order=self.order, row=2, seat=2)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    """Airport"""

    def test_airports_list(self):
        url = reverse("airport:airport-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_airports_detail(self):
        url = reverse("airport:airport-detail", kwargs={"pk": self.airport_1.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], self.airport_1.name)
        self.assertEqual(res.data["closest_big_city"], self.airport_1.closest_big_city)

    def test_unauthorized_access_airports_detail(self):
        client = APIClient()
        url = reverse("airport:airport-detail", kwargs={"pk": self.airport_1.pk})
        res = client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    """Route"""

    def test_routes_list(self):
        url = reverse("airport:route-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_route_detail(self):
        url = reverse("airport:route-detail", kwargs={"pk": self.route.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["distance"], self.route.distance)

    def test_unauthorized_access_route_detail(self):
        client = APIClient()
        url = reverse("airport:route-detail", kwargs={"pk": self.route.pk})
        res = client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    """Airplane_Type"""

    def test_airplane_type_list(self):
        url = reverse("airport:airplanetype-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], self.airplane_type.name)

    def test_airplane_type_detail(self):
        url = reverse("airport:airplanetype-detail", kwargs={"pk": self.airplane_type.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], self.airplane_type.name)

    def test_unauthorized_access_airplane_type_detail(self):
        client = APIClient()
        url = reverse("airport:airplanetype-detail", kwargs={"pk": self.airplane_type.pk})
        res = client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    """Airplane"""

    def test_airplane_list(self):
        url = reverse("airport:airplane-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], self.airplane.name)

    def test_airplane_detail(self):
        url = reverse("airport:airplane-detail", kwargs={"pk": self.airplane.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], self.airplane.name)

    def test_unauthorized_access_airplane_detail(self):
        client = APIClient()
        url = reverse("airport:airplane-detail", kwargs={"pk": self.airplane.pk})
        res = client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    """Order"""

    def test_order_list(self):
        url = reverse("airport:order-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_order_detail(self):
        url = reverse("airport:order-detail", kwargs={"pk": self.order.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_unauthorized_access_order_detail(self):
        client = APIClient()
        url = reverse("airport:order-detail", kwargs={"pk": self.order.pk})
        res = client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    """Ticket"""

    def test_ticket_list(self):
        url = reverse("airport:ticket-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_ticket_detail(self):
        url = reverse("airport:ticket-detail", kwargs={"pk": self.ticket.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_unauthorized_access_ticket_detail(self):
        client = APIClient()
        url = reverse("airport:ticket-detail", kwargs={"pk": self.ticket.pk})
        res = client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    """Flight"""

    def test_flight_list(self):
        url = reverse("airport:flight-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_flight_detail(self):
        url = reverse("airport:flight-detail", kwargs={"pk": self.flight.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_unauthorized_access_flight_detail(self):
        client = APIClient()
        url = reverse("airport:flight-detail", kwargs={"pk": self.flight.pk})
        res = client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    """Crew"""

    def test_crew_list(self):
        url = reverse("airport:crew-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_crew_detail(self):
        url = reverse("airport:crew-detail", kwargs={"pk": self.crew.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["flight"]), 1)
        self.assertEqual(res.data["flight"][0]["route"]["source"]["name"], self.route.source.name)

    def test_unauthorized_access_crew_detail(self):
        client = APIClient()
        url = reverse("airport:crew-detail", kwargs={"pk": self.crew.pk})
        res = client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
