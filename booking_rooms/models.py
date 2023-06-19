import datetime
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


FOCUS, TEAM, CONFERENCE = 'focus', 'team', 'conference'


class Room(models.Model):
    TYPE_CHOICE = (
        (FOCUS, FOCUS),
        (TEAM, TEAM),
        (CONFERENCE, CONFERENCE)
    )
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICE)
    capacity = models.IntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.name}"


class RoomAvailability(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return f"{self.room.name} {self.start}"

    def clean(self):
        today = datetime.date.today()
        if self.start.date() != self.end.date():
            raise ValidationError('Start va end maydonlarini sanasi bir xil bo\'lishi kerak')
        if self.start.date() < today:
            raise ValidationError('Bugundan oldingi kunlari kirita olmaysiz')
        if self.start.time() >= self.end.time():
            raise ValidationError('boshlanish vaqti tugash vaqtidan kichik bo\'lishi kerak')


class BookingRoom(models.Model):
    resident_name = models.CharField(max_length=50,)
    room_availability = models.ForeignKey(RoomAvailability, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.resident_name} {self.room.name}"
