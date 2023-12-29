from rest_framework import viewsets

from airport.models import Crew, AirplaneType, Airplane, Airport, Route, Flight
from airport.serializers import (
    CrewSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer, RouteSerializer, AirportSerializer, FlightSerializer
)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related("route", "airplane").prefetch_related("crew")
    serializer_class = FlightSerializer
