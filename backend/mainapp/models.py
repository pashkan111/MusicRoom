from django.db import models
import random
import string

def make_code():
    l = 6
    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=l))
        if not Room.objects.filter(code=code):
            break
    return code


class Room(models.Model):
    code = models.CharField(max_length=9, unique=True, default=make_code)
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    votes_to_skip = models.IntegerField(default=1)

