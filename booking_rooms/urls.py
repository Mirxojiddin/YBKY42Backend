from django.urls import path

from booking_rooms.views import RoomListApiView, RoomAvailabilityApiView, RoomDetailApiView, \
    BookingRoomApiView
app_name = "booking_rooms"
urlpatterns = [
    path('rooms', RoomListApiView.as_view(), name='rooms'),
    path('rooms/<int:pk>', RoomDetailApiView.as_view(), name='detail'),
    path('rooms/<int:pk>/availability', RoomAvailabilityApiView.as_view(), name='availability'),
    path('rooms/<int:pk>/book', BookingRoomApiView.as_view(), name='book')

]
