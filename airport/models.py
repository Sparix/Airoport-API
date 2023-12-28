from django.db import models


# Create your models here.
class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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
