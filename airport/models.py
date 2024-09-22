import os
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

from airport_service import settings


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.closest_big_city})"


class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='routes_from')
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='routes_to')
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source.name} - {self.destination.name} {self.destination}"


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE, related_name='airplanes')

    def __str__(self):
        return f"name - {self.name}, rows - {self.rows}, seats - {self.seats_in_row}, type - {self.airplane_type}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.created_at} - {self.user.username}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey("Flight", on_delete=models.CASCADE, related_name='tickets')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tickets')


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='flights')
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name='flights')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"{self.route.__str__()} - {self.airplane.name} time ({self.departure_time} - {self.arrival_time})"


def member_picture_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.first_name)}_{slugify(instance.last_name)}_{uuid.uuid4()}{extension}"
    return os.path.join("crews/", filename)


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    picture_member = models.ImageField(upload_to=member_picture_file_path, null=True)
    flight = models.ManyToManyField(Flight)
