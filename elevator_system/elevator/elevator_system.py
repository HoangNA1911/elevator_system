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

    def sort_nearly_elevator(self, floor_number, direction):
        elevator_rank = []
        for elevator in self.elevators:
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
        return sorted(elevator_rank, key=lambda x: x[1])

    def find_best_elevator(
            self, floor_number: int,
            direction: str
    ) -> Elevator | None:
        """Find the best elevator for request by floor number and direction"""
        elevators = self.sort_nearly_elevator(floor_number, direction)
        best_elevator = None

        for elevator, distance in elevators:
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
                        e.status == "idle" for e, _ in elevators):
                    # if distance > 2 and have another free elevator
                    # => add floor into that one
                    idle_elevator = next(
                        (e for e, _ in elevators if e.status == "idle"))
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

        # Append into queue if dont have any elevator available
        if best_elevator is None:
            if (floor_number, direction) not in self.request_queue:
                self.request_queue.append((floor_number, direction))
        return best_elevator

    def step(self):
        """Run for each 2 seconds move all elevator"""
        for elevator in self.elevators:
            elevator.move()
        self.check_request_queue()

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

    def check_request_queue(self):

        if any(e.status == "idle" for e in self.elevators) and self.request_queue:
            for floor_number, direction in self.request_queue:
                elevator = self.find_best_elevator(floor_number,direction)
                if elevator:
                    self.request_queue = [
                        t for t in self.request_queue
                        if t[0] != floor_number
                    ]