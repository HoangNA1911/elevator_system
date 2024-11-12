from time import sleep

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
        default="idle",
    )
    target_direction = models.CharField(
        max_length=4,
        choices=STATUS_CHOICES,
        default="idle",
    )
    target_floors = models.JSONField(default=list, blank=True)
    is_open = models.BooleanField(default=False)

    def move(self):
        # Change direction if elevator at max or min floor
        if self.target_floors:
            if (
                    self.status == "up"
                    and self.current_floor == max(self.target_floors)
                    and self.target_direction == "down"
                    or self.status == "down"
                    and self.current_floor == min(self.target_floors)
                    and self.target_direction == "up"
            ):
                self.status = self.target_direction
            # Remove from target list and open the door

            if (self.current_floor in self.target_floors
                    and self.status == self.target_direction):
                self.target_floors.remove(self.current_floor)
                self.open_door()
                sleep(2)
                self.close_door()
            if not self.target_floors:
                # If elev don't have any request it is idle
                self.status = "idle"
            else:
                # Move elevator 1 floor according to status of them
                if not self.is_open:
                    if self.status == "up":
                        if self.current_floor + 1 <= MAX_FLOOR:
                            self.current_floor += 1
                    elif self.status == "down":
                        if self.current_floor > 0:
                            self.current_floor -= 1
        self.save()

    def open_door(self):
        self.is_open = True
        self.save()

    def close_door(self):
        self.is_open = False
        self.save()

    def add_target_floor(self, floor_number, direction):

        if self.status == "idle":
            # if the elevator is idle set status of elevator by floor
            # and target direction by request
            self.status = "up" if self.current_floor < floor_number else "down"
            self.target_direction = direction

        if (
                floor_number not in self.target_floors and
                self.target_direction == direction
        ):
            # Add floor into target_floor
            self.target_floors.append(floor_number)
        self.save()

    def choose_target_floor(self, floor_number):
        if self.status == "idle":
            self.status = "up" if self.current_floor < floor_number else "down"
            if floor_number not in self.target_floors:
                self.target_floors.append(floor_number)

        if floor_number not in self.target_floors:
            if (
                    floor_number >= self.current_floor
                    and self.status == "up"
                    or floor_number <= self.current_floor
                    and self.status == "down"
            ):
                self.target_floors.append(floor_number)

