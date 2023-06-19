from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import pagination, status
from rest_framework.response import Response
from rest_framework.views import APIView
from booking_rooms.serializers import RoomSerializer
from booking_rooms.models import Room


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
