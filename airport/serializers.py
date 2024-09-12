from rest_framework import serializers

from airport.models import Airport, Route, Airplane, AirplaneType, Order, Ticket, Flight, Crew


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class RouteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteDetailSerializer(RouteListSerializer):
    source = AirportSerializer(read_only=False)
    destination = AirportSerializer(read_only=False)

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type")


class AirplaneDetailSerializer(serializers.ModelSerializer):
    airplane_type = AirplaneTypeSerializer(read_only=False)

    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type")


class OrderListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")

    class Meta:
        model = Order
        fields = ("created_at", "user")


class FlightListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time")


class FlightDetailSerializer(serializers.ModelSerializer):
    route = RouteDetailSerializer()
    airplane = AirplaneDetailSerializer()

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time")


class TicketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight", "order",)


class TicketDetailSerializer(TicketListSerializer):
    flight = FlightDetailSerializer(read_only=False)
    order = OrderListSerializer(read_only=False)

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight", "order")


class CrewSerializer(serializers.ModelSerializer):
    flight = FlightDetailSerializer(read_only=False, many=True)

    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "flight")
