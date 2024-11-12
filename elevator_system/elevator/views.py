from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
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


@api_view(['GET'])
def fetch_elevator(request):
    elevators = Elevator.objects.all()
    data = ElevatorSerializer(elevators, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)


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

    elevator.add_target_floor(floor_number=request_floor, direction=direction)

    elevators = Elevator.objects.all()
    data = ElevatorSerializer(elevators, many=True).data
    return Response(
        {
            "message": "Elevator is coming",
            "elevators": data,
        },
        status=status.HTTP_200_OK,
    )


@csrf_exempt
@api_view(["POST"])
def step(request):
    elevator_system.step()
    elevators = Elevator.objects.all()
    data = ElevatorSerializer(elevators, many=True).data
    return Response(
        {
            "message": "move all elev",
            "elevators": data,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def open_door(request):
    id_elevator = request.data.get("elevator_id")
    elevator_system.open_elevator(elevator_id=id_elevator)
    return Response(
        {"message": "elevator's door is open"},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def close_door(request):
    id_elevator = request.data.get("elevator_id")
    elevator_system.close_elevator(elevator_id=id_elevator)
    return Response(
        {"message": "elevator's door is close"},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def choose_target_floor(request):
    id_elevator = request.data.get("elevator_id")
    floor_number = request.data.get("floor_number")
    elevator_system.choose_target_floor(
        elevator_id=id_elevator,
        floor_number=floor_number,
    )
    return Response(
        {"message": "Elevator is coming"},
        status=status.HTTP_200_OK,
    )


def elevator_control_panel(request):
    return render(request, "elevator/index.html")


