from datetime import datetime, date

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import pagination, status
from rest_framework.response import Response
from rest_framework.views import APIView
from booking_rooms.serializers import RoomSerializer, RoomAvailabilitySerializer, BookingRoomSerializer
from booking_rooms.models import Room, RoomAvailability, BookingRoom


def check_day(pk):
    try:
        room = Room.objects.get(id=pk)
        return room
    except ObjectDoesNotExist:
        data = {
            "message": "Bunday xona topilmadi"
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)


class RoomListApiView(APIView):
    def get(self, request):
        search = request.GET.get('search', 0)
        type_of_room = request.GET.get('type', 0)
        if search and type_of_room:
            rooms = Room.objects.filter(Q(name=search) & Q(type=type_of_room))
        elif type_of_room:
            rooms = Room.objects.filter(type=type_of_room)
        elif search:
            rooms = Room.objects.filter(name=search)
        else:
            rooms = Room.objects.all()
        if rooms.count() < 1:
            data = {
                'message': 'Szi kiritgan parametirlar asosida xonalar topilmadi'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        else:
            paginator = pagination.PageNumberPagination()
            paginator.invalid_page_message = "Siz kiritgan sahifa mavjud emas"
            get_page_size = request.GET.get('page_size', 0)
            paginator.page_size_query_param = 'page_size'
            page_obj = paginator.paginate_queryset(rooms, request)
            serializer = RoomSerializer(page_obj, many=True).data
            current_page = paginator.page.number
            page_size = int(get_page_size) if get_page_size else paginator.page_size
            data = {
                'page': current_page,
                'count': rooms.count(),
                'page_size': page_size,
                'results': serializer
            }
            return Response(data, status=status.HTTP_200_OK)


class RoomDetailApiView(APIView):
    def get(self, request, pk):
        result = check_day(pk)
        if isinstance(result, Room):
            serializer = RoomSerializer(result)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return result


class RoomAvailabilityApiView(APIView):
    def get(self, request, pk):
        dates = request.GET.get('date', 0)
        today = date.today()
        if dates:
            try:
                date_format = '%Y-%m-%d'
                date_obj = datetime.strptime(dates, date_format).date()
                if date_obj < today:
                    data = {
                        "error": "Iltimos bugundan avvalgi kunni kiritmang"
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                data = {
                    "error": "Iltimos 'date' ni yil - oy - kun formatida kiriting"
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            date_obj = today
        result = check_day(pk)
        if isinstance(result, Room):
            room_availability = RoomAvailability.objects.filter(Q(room=result) & Q(date=date_obj))
            if room_availability:
                serializer = RoomAvailabilitySerializer(room_availability, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                data = {
                    "massage": f"Xonaning {date_obj} kuni uchun bosh vaqtlari topilmadi"
                }
                return Response(data, status=status.HTTP_404_NOT_FOUND)
        else:
            return result


class BookingRoomApiView(APIView):
    def post(self, request, pk):
        result = check_day(pk)
        if not isinstance(result, Room):
            return result
        start = request.data.get('start')
        end = request.data.get('end')
        resident = request.data.get('resident')
        if not resident or not (type(resident) is dict):
            return Response(data={
                'error': "Iltimos resident ma'lumotlarini kiriting"
            }, status=status.HTTP_400_BAD_REQUEST)
        elif 'name' not in resident:
            return Response(data={
                'error': "Iltimos resinedtni ismini 'name' orqali kiriting"
            }, status=status.HTTP_400_BAD_REQUEST)
        if not start or not end:
            return Response(data={
                'error': "Iltimos start va end maydonlarni ikkisini ham kitiring"
            }, status=status.HTTP_400_BAD_REQUEST)
        date_format = '%Y-%m-%d %H:%M:%S'
        try:
            start_date = datetime.strptime(start, date_format)
            end_time = datetime.strptime(end, date_format)
        except ValueError:
            data = {
                "error": "Iltimos sanalarnini y-o-k s-d-sek formatida kiriting"
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        serializer = BookingRoomSerializer(data=request.data)
        if serializer.is_valid():
            try:
                available = RoomAvailability.objects.get(room_id=pk, start=start_date,
                                                         end=end_time)
                is_booked = BookingRoom.objects.filter(Q(room_id=pk) & Q(room_availability=available)).count() > 0
                if is_booked:
                    return Response({
                        "error": "Uzr, siz tanlagan vaqtda xona band qilingan"
                    }, status=status.HTTP_410_GONE)
                else:
                    BookingRoom.objects.create(room_id=pk, room_availability=available, resident_name=resident['name'])
                    return Response({
                        "message": "Xona muvaffaqiyatli band qilindi"
                    }, status=status.HTTP_201_CREATED)
            except ObjectDoesNotExist:
                data = {
                    "message": f"Xonaning {start_date.date()} kuni uchun bosh vaqtlari topilmadi"
                }
                return Response(data, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
