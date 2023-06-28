from datetime import datetime, date
import json
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import pagination, status
from rest_framework.response import Response
from rest_framework.views import APIView
from booking_rooms.serializers import RoomSerializer, BookingRoomSerializer
from booking_rooms.models import Room, RoomAvailability, BookingRoom


def check_day(pk):
    try:
        room = Room.objects.get(id=pk)
        return room
    except ObjectDoesNotExist:
        data = {
            "error": "topilmadi"
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


def remove_quotes(datetime_object):
    return datetime_object.strftime("%Y-%m-%d %H:%M:%S")


class RoomAvailabilityApiView(APIView):
    def get(self, request, pk):
        dates = request.GET.get('date', 0)
        today = date.today()
        date_obj1 = date.today().strftime("%d-%m-%Y")
        if dates:
            try:
                date_format = '%d-%m-%Y'
                date_obj = datetime.strptime(dates, date_format).date()
                date_obj1 = datetime.strptime(dates, date_format).date().strftime(date_format)
                if date_obj < today:
                    data = {
                        "error": "Iltimos bugundan avvalgi kunni kiritmang"
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                data = {
                    "error": "Iltimos 'date' ni [%d-%m-Y] formatida kiriting"
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            date_obj = today
        result = check_day(pk)
        if isinstance(result, Room):
            room_availability = BookingRoom.objects.filter(Q(room=result) & Q(start__date=date_obj)).order_by('start')
            if room_availability:
                counter = 0
                date_format = "%d-%m-%Y %H:%M:%S"
                last = room_availability.count()
                start_time = f"{date_obj1} 00:00:00"
                start_date = datetime.strptime(start_time,date_format)

                result = {}

                for i in room_availability:
                    i_start = i.start.strftime(date_format)
                    i_end = i.end.strftime(date_format)
                    if i.start.time() != start_date.time():
                        result[counter] = {
                            "start": start_time,
                            "end": i_start
                            }
                    start_date = i.end
                    start_time = i_end
                    if last == counter+1:
                        if str(i.end.time()) != '23:59:59':
                            result[counter+1] = {
                                "start": start_time,
                                "end": f"{date_obj1} 23:59:59"
                            }
                    counter += 1
                json_string = [i for i in result.values()]
                return Response(data=json_string, status=status.HTTP_200_OK)
            else:
                data = [
                    {
                        "start": f"{date_obj1} 00:00:00",
                        "end": f"{date_obj1} 23:59:59"
                    }
                ]

            return Response(data=data, status=status.HTTP_200_OK)
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
        date_format = '%d-%m-%Y %H:%M:%S'
        try:
            start_date = datetime.strptime(start, date_format)
            end_date = datetime.strptime(end, date_format)
        except ValueError:
            data = {
                "error": "Iltimos sanalarnini [%d-%m-%Y %H:%M:%S] formatida kiriting"
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        serializer = BookingRoomSerializer(data=request.data)
        if serializer.is_valid():
            available = BookingRoom.objects.filter(Q(room_id=pk) & Q(start__date=start_date.date()))
            if available.count() < 1:
                BookingRoom.objects.create(
                    room_id=pk,
                    start=start_date,
                    end=end_date,
                    resident_name=resident['name'])
                return Response({
                    "message": "xona muvaffaqiyatli band qilindi"
                }, status=status.HTTP_201_CREATED)
            else:
                for i in available:
                    if start_date.time() < i.start.time() < end_date.time() \
                            or start_date.time() < i.end.time() < end_date.time() \
                            or (start_date.time() == i.start.time() and end_date.time() == i.end.time()):
                        return Response({
                            "error": "uzr, siz tanlagan vaqtda xona band"
                        }, status=status.HTTP_410_GONE)
                BookingRoom.objects.create(
                    room_id=pk,
                    start=start_date,
                    end=end_date,
                    resident_name=resident['name'])
                return Response({
                    "message": "xona muvaffaqiyatli band qilindi"
                }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
