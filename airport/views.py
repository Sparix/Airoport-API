from rest_framework import viewsets

from airport.models import (
    Crew,
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Flight,
    Order,
    Country,
    City
)
from airport.serializers import (
    CrewSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    RouteSerializer,
    AirportSerializer,
    FlightSerializer,
    AirplaneListSerializer,
    RouteListSerializer,
    FlightListSerializer,
    OrderSerializer,
    OrderListSerializer,
    AirportListSerializer,
    CountrySerializer,
    CitySerializer,
    CityListSerializer
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

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action == "list":
            return AirplaneListSerializer

        return serializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.select_related(
        "closest_big_city__country",
    )
    serializer_class = AirportSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return AirportListSerializer

        return self.serializer_class


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related(
        "source__closest_big_city__country", "destination__closest_big_city__country"
    )
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action in ("list", "retrieve"):
            return RouteListSerializer

        return serializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = flights = Flight.objects.select_related(
        "route__source__closest_big_city__country",
        "route__destination__closest_big_city__country",
        "airplane__airplane_type",
    ).prefetch_related("crew")
    serializer_class = FlightSerializer

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action in ("list", "retrieve"):
            return FlightListSerializer

        return serializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related(
        "tickets__flight__route__source__closest_big_city__country",
        "tickets__flight__route__destination__closest_big_city__country",
        "tickets__flight__airplane__airplane_type",
        "tickets__flight__crew"
    )
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.select_related("country")
    serializer_class = CitySerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return CityListSerializer

        return self.serializer_class
