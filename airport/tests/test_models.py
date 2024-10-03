from django.test import TestCase
from django.contrib.auth import get_user_model
from airport.models import (
    Airport, Route, Airplane, AirplaneType, Order, Ticket, Flight, Crew, member_picture_file_path
)
from uuid import UUID


class ModelsTestCase(TestCase):

    def setUp(self):
        self.airport1 = Airport.objects.create(name="JFK", closest_big_city="New York")
        self.airport2 = Airport.objects.create(name="LAX", closest_big_city="Los Angeles")
        self.airplane_type = AirplaneType.objects.create(name="Boeing 747")
        self.airplane = Airplane.objects.create(name="Boeing", rows=30, seats_in_row=6,
                                                airplane_type=self.airplane_type)
        self.route = Route.objects.create(source=self.airport1, destination=self.airport2, distance=4000)
        self.flight = Flight.objects.create(
            route=self.route, airplane=self.airplane, departure_time="2024-01-01 10:00:00",
            arrival_time="2024-01-01 14:00:00"
        )
        self.user = get_user_model().objects.create(email="admin@.com")
        self.order = Order.objects.create(user=self.user)
        self.ticket = Ticket.objects.create(row=5, seat=10, flight=self.flight, order=self.order)

    # Test Airport model
    def test_airport_str(self):
        self.assertEqual(str(self.airport1), "JFK (New York)")
        self.assertEqual(str(self.airport2), "LAX (Los Angeles)")

    # Test Route model
    def test_route_str(self):
        self.assertEqual(str(self.route), "JFK - LAX Los Angeles")

    # Test AirplaneType model
    def test_airplane_type_str(self):
        self.assertEqual(str(self.airplane_type), "Boeing 747")

    # Test Airplane model
    def test_airplane_str(self):
        self.assertEqual(
            str(self.airplane),
            "name - Boeing, rows - 30, seats - 6, type - Boeing 747"
        )

    # Test Order model
    def test_order_str(self):
        self.assertEqual(str(self.order), f"{self.order.created_at} - admin@.com")

    # Test Flight model
    def test_flight_str(self):
        self.assertEqual(
            str(self.flight),
            "JFK - LAX (Los Angeles) - Boeing time (2024-01-01 10:00:00 - 2024-01-01 14:00:00)"
        )

    # Test Crew model
    def test_crew_creation(self):
        crew_member = Crew.objects.create(first_name="John", last_name="Doe")
        crew_member.flight.add(self.flight)
        self.assertIn(self.flight, crew_member.flight.all())

    # Test Ticket model
    def test_ticket_creation(self):
        self.assertEqual(self.ticket.row, 5)
        self.assertEqual(self.ticket.seat, 10)
        self.assertEqual(self.ticket.flight, self.flight)
        self.assertEqual(self.ticket.order, self.order)

    # Test member_picture_file_path function
    def test_member_picture_file_path(self):
        class MockMember:
            first_name = "John"
            last_name = "Doe"

        instance = MockMember()
        filename = "photo.jpg"
        path = member_picture_file_path(instance, filename)

        # Check if the path is correctly formatted
        self.assertTrue(path.startswith("crews/john_doe_"))
        self.assertTrue(path.endswith(".jpg"))

        # Extract UUID from the generated filename and check if it's valid
        uuid_part = path.split("_")[-1].split(".")[0]
        try:
            UUID(uuid_part)
            valid_uuid = True
        except ValueError:
            valid_uuid = False

        self.assertTrue(valid_uuid)
