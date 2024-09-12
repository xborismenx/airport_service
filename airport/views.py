from django.shortcuts import render
from rest_framework import viewsets

from airport.models import Airport, Route, AirplaneType, Airplane, Order, Ticket, Flight, Crew
from airport.serializers import (AirportSerializer, RouteListSerializer, AirplaneTypeSerializer, AirplaneListSerializer,
                                 TicketListSerializer, FlightListSerializer, CrewSerializer, RouteDetailSerializer,
                                 AirplaneDetailSerializer, OrderListSerializer, TicketDetailSerializer,
                                 FlightDetailSerializer)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related('source', 'destination')
    serializer_class = RouteListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RouteDetailSerializer
        return RouteListSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AirplaneDetailSerializer
        return AirplaneListSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().select_related("flight__route__source", "flight__route__destination", "order__user")
    serializer_class = TicketListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TicketDetailSerializer
        return TicketListSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all().select_related("route__destination")
    serializer_class = FlightListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FlightDetailSerializer
        return FlightListSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
