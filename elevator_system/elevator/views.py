from django.shortcuts import render
from rest_framework import viewsets

from .serializers import ElevatorSerializer
from .models import Elevator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ElevatorSerializer
from django.http import HttpRequest
from .elevator_system import ElevatorSystem

from .elevator_system import ElevatorSystem
# Create your views here.

elevator_system = ElevatorSystem()
class ElevatorViewSet(viewsets.ModelViewSet):

    serializer_class = ElevatorSerializer
    queryset = Elevator.objects.all()


@api_view(['POST'])
def call_elevator(request):
    """Find the best elevator and append floor number into target list"""

    request_floor = request.data.get("floor_number")
    direction = request.data.get("direction")
    print(request_floor, direction)

    # Find the best elevator using your ElevatorSystem class
    elevator = elevator_system.find_best_elevator(
        floor_number=request_floor,
        direction=direction,
    )

    if not elevator.target_floors:
        elevator.status = "down" if elevator.status == "up" else "up"

    elevator.add_target_floor(floor_number=request_floor)

    return Response({"message": "Elevator is coming"},
                    status=status.HTTP_200_OK)


