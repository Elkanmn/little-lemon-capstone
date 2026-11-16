from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class MenuItem(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    inventory = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=60, default="Main")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.title} (${self.price})"


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    name = models.CharField(max_length=120)
    email = models.EmailField()
    no_of_guests = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    booking_date = models.DateField()
    booking_time = models.TimeField()
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["booking_date", "booking_time", "id"]

    def __str__(self):
        return f"{self.name}: {self.booking_date} {self.booking_time}"
