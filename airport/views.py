from rest_framework import viewsets

from airport.models import Airport, Route, AirplaneType, Airplane, Order, Ticket, Flight, Crew
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
from airport.serializers import (AirportSerializer, RouteListSerializer, AirplaneTypeSerializer, AirplaneListSerializer,
                                 TicketListSerializer, FlightListSerializer, CrewListSerializer, RouteDetailSerializer,
                                 AirplaneDetailSerializer, OrderListSerializer, TicketDetailSerializer,
                                 FlightDetailSerializer, CrewDetailSerializer)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related('source', 'destination')
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RouteDetailSerializer
        return RouteListSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AirplaneDetailSerializer
        return AirplaneListSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related("user")
    serializer_class = OrderListSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().select_related("flight__route__source", "flight__route__destination", "order__user")
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TicketDetailSerializer
        return TicketListSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all().select_related("route__destination", "airplane")
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FlightDetailSerializer
        return FlightListSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all().prefetch_related("flight__route__destination")
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CrewDetailSerializer
        return CrewListSerializer
