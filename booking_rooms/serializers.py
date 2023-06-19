from datetime import date
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from booking_rooms.models import BookingRoom, Room, RoomAvailability


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'type', 'capacity')


class RoomAvailabilitySerializer(serializers.ModelSerializer):
    room = RoomSerializer(write_only=True)
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = RoomAvailability
        fields = ('start', 'end')


class BookingRoomSerializer(serializers.ModelSerializer):
    resident = serializers.DictField(
        child=serializers.CharField())
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()

    class Meta:
        model = BookingRoom
        fields = ("resident", 'start', 'end')

    def validate(self, data):
        start = data.get('start')
        end = data.get('end')
        start_time = start.time()
        end_time = end.time()
        start_date = start.date()
        end_date = end.date()
        today = date.today()
        if start_date != end_date:
            raise ValidationError(
                {
                    "error": "start va end ga kiritayotgan kunlari bir xil bo'lishi kerak"
                }
            )

        if start_date < today or end_date < today:
            data = {
                "error": "Iltimos bugundan avvalgi kunni kiritmang"
            }
            raise ValidationError(data)

        if start_time > end_time:
            raise ValidationError(
                {
                    "error": "start ning vaqti  endning vaqtidan kichik bo'lishi kerak"
                }
            )

        return data

