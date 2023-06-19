from datetime import datetime

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from booking_rooms.models import Room, RoomAvailability


class RoomListApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.room_one = Room.objects.create(name='new', type='conference', capacity=15)
        self.room_two = Room.objects.create(name='old', type='team', capacity=8)
        self.room_three = Room.objects.create(name='again', type='focus', capacity=1)

    def test_rooms_list(self):
        response = self.client.get(reverse("booking_rooms:rooms"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['results'][0]['id'], self.room_one.id)
        self.assertEqual(response.data['results'][0]['name'], self.room_one.name)
        self.assertEqual(response.data['results'][0]['type'], self.room_one.type)
        self.assertEqual(response.data['results'][0]['capacity'], self.room_one.capacity)
        self.assertEqual(response.data['results'][1]['id'], self.room_two.id)
        self.assertEqual(response.data['results'][1]['name'], self.room_two.name)
        self.assertEqual(response.data['results'][1]['type'], self.room_two.type)
        self.assertEqual(response.data['results'][1]['capacity'], self.room_two.capacity)
        self.assertEqual(response.data['results'][2]['id'], self.room_three.id)
        self.assertEqual(response.data['results'][2]['name'], self.room_three.name)
        self.assertEqual(response.data['results'][2]['type'], self.room_three.type)
        self.assertEqual(response.data['results'][2]['capacity'], self.room_three.capacity)
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(response.data['page'], 1)
        self.assertEqual(response.data['page_size'], 10)

    def test_room_page_size_list(self):
        response = self.client.get(reverse("booking_rooms:rooms") + '?page_size=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['id'], self.room_one.id)
        self.assertEqual(response.data['results'][0]['name'], self.room_one.name)
        self.assertEqual(response.data['results'][0]['type'], self.room_one.type)
        self.assertEqual(response.data['results'][0]['capacity'], self.room_one.capacity)
        self.assertEqual(response.data['results'][1]['id'], self.room_two.id)
        self.assertEqual(response.data['results'][1]['name'], self.room_two.name)
        self.assertEqual(response.data['results'][1]['type'], self.room_two.type)
        self.assertEqual(response.data['results'][1]['capacity'], self.room_two.capacity)
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(response.data['page'], 1)
        self.assertEqual(response.data['page_size'], 2)

    def test_room_page_list(self):
        # page not found
        response = self.client.get(reverse("booking_rooms:rooms") + '?page=2')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Siz kiritgan sahifa mavjud emas')

        # page_size => page not found
        response = self.client.get(reverse("booking_rooms:rooms") + '?page=3&page_size=2')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Siz kiritgan sahifa mavjud emas')

        # list
        response = self.client.get(reverse("booking_rooms:rooms") + '?page_size=2&page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], self.room_three.id)
        self.assertEqual(response.data['results'][0]['name'], self.room_three.name)
        self.assertEqual(response.data['results'][0]['type'], self.room_three.type)
        self.assertEqual(response.data['results'][0]['capacity'], self.room_three.capacity)
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(response.data['page'], 2)
        self.assertEqual(response.data['page_size'], 2)

    def test_room_search_list(self):
        # search not found
        response = self.client.get(reverse("booking_rooms:rooms") + '?search=mytaxi')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['message'], 'Szi kiritgan parametirlar asosida xonalar topilmadi')

        # search list
        response = self.client.get(reverse("booking_rooms:rooms") + '?search=again')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], self.room_three.id)
        self.assertEqual(response.data['results'][0]['name'], self.room_three.name)
        self.assertEqual(response.data['results'][0]['type'], self.room_three.type)
        self.assertEqual(response.data['results'][0]['capacity'], self.room_three.capacity)

        # search list
        response = self.client.get(reverse("booking_rooms:rooms") + '?search=old')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], self.room_two.id)
        self.assertEqual(response.data['results'][0]['name'], self.room_two.name)
        self.assertEqual(response.data['results'][0]['type'], self.room_two.type)
        self.assertEqual(response.data['results'][0]['capacity'], self.room_two.capacity)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['page'], 1)
        self.assertEqual(response.data['page_size'], 10)

    def test_room_type_list(self):
        # type not found
        response = self.client.get(reverse("booking_rooms:rooms") + '?type=comfort')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['message'], 'Szi kiritgan parametirlar asosida xonalar topilmadi')
        # type list
        response = self.client.get(reverse("booking_rooms:rooms") + '?type=conference')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], self.room_one.id)
        self.assertEqual(response.data['results'][0]['name'], self.room_one.name)
        self.assertEqual(response.data['results'][0]['type'], self.room_one.type)
        self.assertEqual(response.data['results'][0]['capacity'], self.room_one.capacity)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['page'], 1)
        self.assertEqual(response.data['page_size'], 10)
        # type + search not found
        response = self.client.get(reverse("booking_rooms:rooms") + '?type=conference&search=old')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['message'], 'Szi kiritgan parametirlar asosida xonalar topilmadi')

        # type+search list
        response = self.client.get(reverse("booking_rooms:rooms") + '?type=conference&search=new')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], self.room_one.id)
        self.assertEqual(response.data['results'][0]['name'], self.room_one.name)
        self.assertEqual(response.data['results'][0]['type'], self.room_one.type)
        self.assertEqual(response.data['results'][0]['capacity'], self.room_one.capacity)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['page'], 1)
        self.assertEqual(response.data['page_size'], 10)


class RoomDetailApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.room_one = Room.objects.create(name='new', type='conference', capacity=15)
        self.room_two = Room.objects.create(name='old', type='team', capacity=8)
        self.room_three = Room.objects.create(name='again', type='focus', capacity=1)

    def test_room_detail(self):
        # room not found
        response = self.client.get(reverse("booking_rooms:detail", kwargs={"pk": 10}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['message'], 'Bunday xona topilmadi')

        # room detail
        response = self.client.get(reverse("booking_rooms:detail", kwargs={"pk": self.room_two.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data['id'], self.room_two.id)
        self.assertEqual(response.data['name'], self.room_two.name)
        self.assertEqual(response.data['type'], self.room_two.type)
        self.assertEqual(response.data['capacity'], self.room_two.capacity)

        # room detail
        response = self.client.get(reverse("booking_rooms:detail", kwargs={"pk": self.room_three.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data['id'], self.room_three.id)
        self.assertEqual(response.data['name'], self.room_three.name)
        self.assertEqual(response.data['type'], self.room_three.type)
        self.assertEqual(response.data['capacity'], self.room_three.capacity)


class RoomAvailabilityTestCase(APITestCase):
    def setUp(self) -> None:
        self.room_one = Room.objects.create(name='new', type='conference', capacity=15)
        self.room_two = Room.objects.create(name='old', type='team', capacity=8)
        date = datetime.date.today() + datetime.timedelta(days=10)
        self.room_availability_one = RoomAvailability.objects.create(room=self.room_one, start=f'{date} 8:00:00',
                                                                     end=f'{date} 10:00:00')
        self.room_availability_two = RoomAvailability.objects.create(room=self.room_one, start=f'{date} 10:00:00',
                                                                     end=f'{date} 11:00:00')

    def test_room_availability_error(self):
        # room not found
        response = self.client.get(reverse("booking_rooms:availability", kwargs={"pk": 10}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['message'], 'Bunday xona topilmadi')

        # bad date format
        response = self.client.get(
            reverse("booking_rooms:availability", kwargs={"pk": self.room_one.id}) + '?date=06-07-2023')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], "Iltimos 'date' ni yil - oy - kun formatida kiriting")

        # date < today
        response = self.client.get(
            reverse("booking_rooms:availability", kwargs={"pk": self.room_one.id}) + '?date=2023-05-05')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], "Iltimos bugundan avvalgi kunni kiritmang")

    def room_availability_list(self):
        # date time not found
        today = datetime.date.today() + datetime.timedelta(days=10)
        response = self.client.get(
            reverse("booking_rooms:availability", kwargs={"pk": self.room_one.id}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['message'], f"Xonaning {today} kuni uchun bosh vaqtlari topilmadi")

        # list
        date_to_search = datetime.date.today() + datetime.timedelta(days=10)
        response = self.client.get(
            reverse("booking_rooms:availability", kwargs={"pk": self.room_one.id}), f"?date={date_to_search}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['date'], self.room_availability_one.date)
        self.assertEqual(response.data[0]['start'], self.room_availability_one.start)
        self.assertEqual(response.data[0]['end'], self.room_availability_one.end)
        self.assertEqual(response.data[1]['date'], self.room_availability_two.date)
        self.assertEqual(response.data[1]['start'], self.room_availability_two.start)
        self.assertEqual(response.data[1]['end'], self.room_availability_two.end)
