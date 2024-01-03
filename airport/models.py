from django.conf import settings
from django.db import models
from rest_framework.exceptions import ValidationError


class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ("last_name",)


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f"City: {self.name}, Country: {self.country.name}"


class AirplaneType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType,
        on_delete=models.CASCADE,
        related_name="airplane"
    )

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return (
            f"Name: {self.name}"
            f"Capacity: {self.capacity}"
            f"Airplane Type: {self.airplane_type}"
        )

    class Meta:
        ordering = ("airplane_type", "rows", "seats_in_row")


class Airport(models.Model):
    name = models.CharField(max_length=255, unique=True)
    closest_big_city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="source_routes"
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="destination_routes"
    )
    distance = models.IntegerField()

    def __str__(self):
        return (
            f"Source: {self.source.name}"
            f"Destination: {self.destination.name}"
        )


class Flight(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="route_flights"
    )
    airplane = models.ForeignKey(
        Airplane,
        on_delete=models.CASCADE,
        related_name="airplane_flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, blank=True)

    def __str__(self):
        return (
            f"Source: {self.route.source.name} "
            f"Destination: {self.route.destination.name}"
        )

    class Meta:
        ordering = ("-departure_time", "-arrival_time",)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ("-created_at",)


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    @staticmethod
    def validate_ticket(row, seat, flight, error):
        for ticket_attr_value, ticket_attr_name, flight_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(flight, flight_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                                          f"number must be in available range: "
                                          f"(1, {flight_attr_name}): "
                                          f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.flight.airplane,
            ValidationError,
        )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    class Meta:
        unique_together = ("row", "seat", "flight",)
        ordering = ("row", "seat",)
