from django.contrib import admin
from .models import Booking, MenuItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "inventory")
    search_fields = ("title", "description")
    list_filter = ("category",)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "booking_date", "booking_time", "no_of_guests")
    search_fields = ("name", "email", "user__username")
    list_filter = ("booking_date",)
