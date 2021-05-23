from django.urls import path
from .views import (RoomView, RoomCreateView, get_room, room_join, leave_room,
UserInRoom, test)
# check_user)

urlpatterns = [
    path('rooms/', RoomView.as_view()),
    # path('test/', test),
    path('room-create/', RoomCreateView.as_view()),
    path('room/', get_room),
    path('room-join/', room_join),
    path('check-user/', UserInRoom.as_view()),
    # path('check-user/', check_user),
    path('leave-room/', leave_room),
    path('test/', test),
]
