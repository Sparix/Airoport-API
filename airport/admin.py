from django.contrib import admin

from airport.models import (
    Crew,
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Flight,
    Order,
    Ticket,
    Country,
    City
)


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name")
    search_fields = ("last_name",)


@admin.register(AirplaneType)
class AirplaneTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ("name", "rows", "seats_in_row", "airplane_type",)
    search_fields = ("airplane_type", "name",)


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ("name", "closest_big_city",)
    search_fields = ("closest_big_city",)


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("source", "destination", "distance",)


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ("route", "airplane", "departure_time", "arrival_time",)
    filter_fields = ("route", "airplane",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("row", "seat", "flight")


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
