from django.http.response import JsonResponse
from django.shortcuts import render
from .serialisers import *
from rest_framework import generics, status
from .models import*
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerialiser


class RoomCreateView(APIView):
    serializer_class = RoomCreateSerialiser

    def post(self, request, format=None):
        if not request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
                request.session['room_code'] = room.code
                print(f'{request.session["room_code"]} created')
                return Response(RoomSerialiser(room).data, status=status.HTTP_200_OK)
            else:
                room = Room(host=host, guest_can_pause=guest_can_pause,
                            votes_to_skip=votes_to_skip)
                room.save()
                request.session['room_code'] = room.code
                print(f'{request.session["room_code"]} created')
                print(request.session.values())
                return Response(RoomSerialiser(room).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_room(request):
    code = request.GET.get('code')
    if code:
        room = Room.objects.filter(code = code)
        if room:
            data = RoomSerialiser(room[0]).data
            data['is_host'] = request.session.session_key == room[0].host
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'Bad Request': 'Room not found'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'Bad Request': 'Code not passed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def room_join(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    code = request.data['code']
    if code != None:
        room = Room.objects.filter(code=code)
        if len(room) > 0:
            request.session['room_code'] = code
            print(f'{request.session["room_code"]} join')
            print(request.session.values())
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        return Response({'Room not found': 'Room not found'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'Code not found': 'Code not found'}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["GET"])
# def check_user(request):
#     if not request.session.exists(request.session.session_key):
#         request.session.create()

#     # code = request.session.get('room_code')
#     code = request.session.get('room_code')
#     print(code)
#     print(request.session.get('y'))

#     data = {
#         'code': code
#     }
#     #     return JsonResponse(data)
#     # else:
#     return JsonResponse({'st': 'no'})

class UserInRoom(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        data = {
            'code': self.request.session.get('room_code')
        }
        print(data)
        return JsonResponse(data, status=status.HTTP_200_OK)

class UpdateRoom(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        data = {
            'code': self.request.session.get('room_code')
        }
        print(data)
        return JsonResponse(data, status=status.HTTP_200_OK)

@api_view(["POST"])
def leave_room(request):
    if 'room_code' in request.session:
        request.session.pop('room_code')
        host = request.session.session_key
        room = Room.objects.filter(host=host)
        if room:
            room.delete()
    print(request.session.values())
    return Response({'status': 'Logged out'})

@api_view(["POST"])
def test(request):
    d = request.data['up']
    print(request.session.values())
    request.session['q'] = d
    return Response({'st':'ok'})