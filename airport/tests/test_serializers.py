from django.test import TestCase
from django.utils import timezone
import datetime

from airport.models import Airport, Route, AirplaneType, Airplane, Order, Flight, Ticket, Crew
from airport.serializers import (
    AirportSerializer, RouteListSerializer, RouteDetailSerializer, OrderListSerializer,
    AirplaneDetailSerializer, AirplaneListSerializer, AirplaneTypeSerializer, FlightListSerializer,
    FlightDetailSerializer, TicketListSerializer, TicketDetailSerializer, CrewDetailSerializer, CrewListSerializer
)
from user.models import User


class SerializersTestCase(TestCase):
    def setUp(self):
        self.airport = Airport.objects.create(name="JFK", closest_big_city="New York")
        self.destination_airport = Airport.objects.create(name="LAX", closest_big_city="Los Angeles")
        self.route = Route.objects.create(source=self.airport, destination=self.destination_airport, distance=2451)
        self.airplane_type = AirplaneType.objects.create(name="Boeing 737")
        self.airplane = Airplane.objects.create(name="Airplane 1", rows=30, seats_in_row=6,
                                                airplane_type=self.airplane_type)
        self.user = User.objects.create_user(email="testuser@example.com", password="password")
        self.order = Order.objects.create(user=self.user)

        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=timezone.make_aware(datetime.datetime(2024, 9, 30, 19, 23, 45)),
            arrival_time=timezone.make_aware(datetime.datetime(2024, 9, 30, 23, 0, 0))
        )
        self.ticket = Ticket.objects.create(row=1, seat=1, flight=self.flight, order=self.order)
        self.crew_member = Crew.objects.create(first_name="John", last_name="Doe", picture_member="path/to/picture.jpg")
        self.crew_member.flight.add(self.flight)

    def test_airport_serializer(self):
        serializer = AirportSerializer(instance=self.airport)
        expected_data = {
            "id": self.airport.id,
            "name": "JFK",
            "closest_big_city": "New York",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_route_list_serializer(self):
        serializer = RouteListSerializer(instance=self.route)
        expected_data = {
            "id": self.route.id,
            "source": self.route.source.id,
            "destination": self.destination_airport.id,
            "distance": self.route.distance,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_route_detail_serializer(self):
        serializer = RouteDetailSerializer(instance=self.route)
        expected_data = {
            "id": self.route.id,
            "source": {
                "id": self.airport.id,
                "name": "JFK",
                "closest_big_city": "New York",
            },
            "destination": {
                "id": self.destination_airport.id,
                "name": "LAX",
                "closest_big_city": "Los Angeles",
            },
            "distance": 2451,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_airplane_type_serialization(self):
        serializer = AirplaneTypeSerializer(instance=self.airplane_type)
        expected_data = {
            "id": self.airplane_type.id,
            "name": "Boeing 737",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_airplane_list_serialization(self):
        serializer = AirplaneListSerializer(instance=self.airplane)
        expected_data = {
            "id": self.airplane.id,
            "name": "Airplane 1",
            "rows": 30,
            "seats_in_row": 6,
            "airplane_type": self.airplane_type.id,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_airplane_detail_serialization(self):
        serializer = AirplaneDetailSerializer(instance=self.airplane)
        expected_data = {
            "id": self.airplane.id,
            "name": "Airplane 1",
            "rows": 30,
            "seats_in_row": 6,
            "airplane_type": {
                "id": self.airplane_type.id,
                "name": "Boeing 737",
            },
        }
        self.assertEqual(serializer.data, expected_data)

    def test_order_list_serialization(self):
        serializer = OrderListSerializer(instance=self.order)
        expected_data = {
            "created_at": self.order.created_at.strftime(format="%Y-%m-%d %H:%M:%S"),  # Use ISO format for datetime
            "customer": "testuser@example.com",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_flight_list_serialization(self):
        serializer = FlightListSerializer(instance=self.flight)
        expected_data = {
            "id": self.flight.id,
            "route": self.route.id,
            "airplane": self.airplane.id,
            "departure_time": self.flight.departure_time.strftime(format="%Y-%m-%d %H:%M:%S"),  # Use ISO format
            "arrival_time": self.flight.arrival_time.strftime(format="%Y-%m-%d %H:%M:%S"),  # Use ISO format
        }
        self.assertEqual(serializer.data, expected_data)

    def test_flight_detail_serialization(self):
        serializer = FlightDetailSerializer(instance=self.flight)
        expected_data = {
            "id": self.flight.id,
            "route": {
                "id": self.route.id,
                "source": {
                    "id": self.airport.id,
                    "name": "JFK",
                    "closest_big_city": "New York",
                },
                "destination": {
                    "id": self.destination_airport.id,
                    "name": "LAX",
                    "closest_big_city": "Los Angeles",
                },
                "distance": 2451,
            },
            "airplane": {
                "id": self.airplane.id,
                "name": "Airplane 1",
                "rows": 30,
                "seats_in_row": 6,
                "airplane_type": {
                    "id": self.airplane_type.id,
                    "name": "Boeing 737",
                },
            },
            "departure_time": self.flight.departure_time.strftime(format="%Y-%m-%d %H:%M:%S"),  # Use ISO format
            "arrival_time": self.flight.arrival_time.strftime(format="%Y-%m-%d %H:%M:%S"),  # Use ISO format
        }
        self.assertEqual(serializer.data, expected_data)

    def test_ticket_list_serialization(self):
        serializer = TicketListSerializer(instance=self.ticket)
        expected_data = {
            "id": self.ticket.id,
            "row": 1,
            "seat": 1,
            "flight": self.flight.id,
            "order": self.order.id,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_ticket_detail_serialization(self):
        serializer = TicketDetailSerializer(instance=self.ticket)
        expected_data = {
            "id": self.ticket.id,
            "row": 1,
            "seat": 1,
            "flight": {
                "id": self.flight.id,
                "route": {
                    "id": self.route.id,
                    "source": {
                        "id": self.airport.id,
                        "name": "JFK",
                        "closest_big_city": "New York",
                    },
                    "destination": {
                        "id": self.destination_airport.id,
                        "name": "LAX",
                        "closest_big_city": "Los Angeles",
                    },
                    "distance": 2451,
                },
                "airplane": {
                    "id": self.airplane.id,
                    "name": "Airplane 1",
                    "rows": 30,
                    "seats_in_row": 6,
                    "airplane_type": {
                        "id": self.airplane_type.id,
                        "name": "Boeing 737",
                    },
                },
                "departure_time": self.flight.departure_time.strftime(format="%Y-%m-%d %H:%M:%S"),  # Use ISO format
                "arrival_time": self.flight.arrival_time.strftime(format="%Y-%m-%d %H:%M:%S"),  # Use ISO format
            },
            "order": {
                "created_at": self.order.created_at.strftime(format="%Y-%m-%d %H:%M:%S"),  # Use ISO format for datetime
                "customer": "testuser@example.com",
            },
        }
        self.assertEqual(serializer.data, expected_data)

    def test_crew_list_serialization(self):
        serializer = CrewListSerializer(instance=self.crew_member)
        expected_data = {
            "id": self.crew_member.id,
            "first_name": "John",
            "last_name": "Doe",
            "flight": [self.flight.id],
            "picture_member": "/path/to/picture.jpg",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_crew_detail_serialization(self):
        serializer = CrewDetailSerializer(instance=self.crew_member)
        expected_data = {
            "id": self.crew_member.id,
            "first_name": "John",
            "last_name": "Doe",
            "flight": [
                {
                    "id": self.flight.id,
                    "route": {
                        "id": self.route.id,
                        "source": {
                            "id": self.airport.id,
                            "name": "JFK",
                            "closest_big_city": "New York",
                        },
                        "destination": {
                            "id": self.destination_airport.id,
                            "name": "LAX",
                            "closest_big_city": "Los Angeles",
                        },
                        "distance": 2451,
                    },
                    "airplane": {
                        "id": self.airplane.id,
                        "name": "Airplane 1",
                        "rows": 30,
                        "seats_in_row": 6,
                        "airplane_type": {
                            "id": self.airplane_type.id,
                            "name": "Boeing 737",
                        },
                    },
                    "departure_time": self.flight.departure_time.strftime(format="%Y-%m-%d %H:%M:%S"),  # Use ISO format
                    "arrival_time": self.flight.arrival_time.strftime(format="%Y-%m-%d %H:%M:%S"),  # Use ISO format
                }
            ],
            "picture_member": "/path/to/picture.jpg",
        }
        self.assertEqual(serializer.data, expected_data)
