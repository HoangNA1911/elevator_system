from django.db import models
# Create your models here.


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
        pass

    def open_door(self):
        self.is_open = True
        self.save()

    def close_door(self):
        self.is_open = False
        self.save()

    def add_target_floor(self, floor_number):

        if floor_number not in self.target_floors:
            self.target_floors.append(floor_number)
