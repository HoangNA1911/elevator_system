from django.db import models
from django.db.models import IntegerField

# Create your models here.

MAX_FLOOR = 10

class Elevator(models.Model):
    STATUS_CHOICES = [
        ('up', 'Up'),
        ('down', 'Down'),
        ('idle', 'Idle'),
    ]

    id = models.IntegerField(primary_key=True)
    current_floor = models.IntegerField(default=1)
    status = models.CharField(
        max_length=4,
        choices=STATUS_CHOICES,
        default='idle',
    )
    target_floors = models.JSONField(default=list, blank=True)
    is_open = models.BooleanField(default=False)

    def move(self):
        if self.target_floors:
            if self.status == "up":
                if self.current_floor + 1 <= MAX_FLOOR:
                    self.current_floor += 1
            elif self.status == "down":
                if self.current_floor > 0:
                    self.current_floor -= 1

        if self.current_floor in self.target_floors:
            self.target_floors.remove(self.current_floor)
        if not self.target_floors:
            self.status = "idle"

        self.save()




    def open_door(self):
        self.is_open = True
        self.save()

    def close_door(self):
        self.is_open = False
        self.save()

    def add_target_floor(self, floor_number):

        if floor_number not in self.target_floors:
            self.target_floors.append(floor_number)
