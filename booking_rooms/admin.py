from django.contrib import admin
from booking_rooms.models import Room, RoomAvailability, BookingRoom


admin.site.register(Room)
admin.site.register(RoomAvailability)
admin.site.register(BookingRoom)

