from .models import Elevator


class ElevatorSystem:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = (super(ElevatorSystem, cls)
                             .__new__(cls, *args, **kwargs))
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.elevators = Elevator.objects.all()
            self.request_queue = []  # If there are no elev => push into  queue

    def find_best_elevator(
            self, floor_number: int,
            direction: str
    ) -> Elevator | None:
        """Find the best elevator for request by floor number and direction"""
        elevator_rank = []
        best_elevator = None
        for elevator in self.elevators:
            best_elevator = elevator
            distance = 0
            if (not elevator.target_floors) or elevator.status == direction:
                distance = abs(elevator.current_floor - floor_number)
            else:
                if elevator.status == "down" and direction == "up":
                    distance = elevator.current_floor + floor_number - (
                                2 * min(elevator.target_floors))
                elif elevator.status == "up" and direction == "down":
                    distance = (2 * max(
                        elevator.target_floors)) - elevator.current_floor - floor_number
            elevator_rank.append((elevator, distance))
        elevator_rank = sorted(elevator_rank, key=lambda x: x[1])
        print(elevator_rank)

        for elevator, distance in elevator_rank:
            if (
                    elevator.current_floor == floor_number
                    and elevator.status == direction
                    or elevator.current_floor == floor_number
                    and elevator.status == "idle"
            ):
                # If the elevator in request floor and
                elevator.add_target_floor(
                    floor_number=floor_number,
                    direction=direction,
                )
                best_elevator = elevator
                break
            elif (
                    elevator.current_floor < floor_number
                    and elevator.status == "up"
                    and direction == "up"
                    or elevator.current_floor > floor_number
                    and elevator.status == "down"
                    and direction == "down"
            ):
                if distance <= 2:
                    elevator.add_target_floor(
                        floor_number=floor_number,
                        direction=direction,
                    )
                    best_elevator = elevator
                    break
                elif distance > 2 and any(
                        e.status == "idle" for e, _ in elevator_rank):
                    # if distance > 2 and have another free elevator
                    # => add floor into that one
                    idle_elevator = next(
                        (e for e, _ in elevator_rank if e.status == "idle"))
                    idle_elevator.add_target_floor(
                        floor_number=floor_number,
                        direction=direction,
                    )
            elif (
                    elevator.current_floor > floor_number
                    and distance <= 2
                    and elevator.status == "down"
                    and direction == "up"
                    or elevator.current_floor < floor_number
                    and distance <= 2
                    and elevator.status == "up"
                    and direction == "down"
            ):
                elevator.add_target_floor(
                    floor_number=floor_number,
                    direction=direction,
                )
                best_elevator = elevator
                break
            elif elevator.status == "idle":
                elevator.add_target_floor(
                    floor_number=floor_number,
                    direction=direction,
                )
                best_elevator = elevator
                break
        self.request_queue.append((floor_number, direction))
        return best_elevator

    def step(self):
        """Run for each 2 seconds move all elevator"""
        for elevator in self.elevators:
            print(
                elevator.status,
                elevator.current_floor,
                elevator.target_floors,
                elevator.target_direction
            )
            elevator.move()

    def open_elevator(self, elevator_id):
        for e in self.elevators:
            if e.id == elevator_id:
                e.open_door()

    def close_elevator(self, elevator_id):
        for e in self.elevators:
            if e.id == elevator_id:
                e.close_door()

    def choose_target_floor(self, elevator_id, floor_number):
        for e in self.elevators:
            if e.id == elevator_id:
                e.choose_target_floor(floor_number=floor_number)
