document.addEventListener("DOMContentLoaded", () => {
    moveAndFetchElevatorData();
    setInterval(moveAndFetchElevatorData, 500);
});

function moveAndFetchElevatorData() {
    fetch('/api/step/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error moving elevators');
            }
            return fetchElevatorData();
        })
        .catch(error => console.error('Error moving elevators:', error));
}

function fetchElevatorData() {
    fetch('/api/fetch-data/')
        .then(response => response.json())
        .then(data => renderElevators(data))
        .catch(error => console.error('Error fetching elevator data:', error));
}

function renderControl() {
    const controlContainer = document.getElementById('control')
    controlContainer.innerHTML = '';
    const controlDiv = document.createElement('div');
    controlDiv.classList.add('control');
    for (let floor = 10; floor >=1; floor--) {
        const floorDiv = document.createElement('div');
        floorDiv.classList.add('floor');

        if (floor < 10) {
            const upArrow = document.createElement('button');
            upArrow.textContent = '↑';
            upArrow.classList.add('arrow', 'up-arrow');
            upArrow.addEventListener('click', () => {
                callElevator(floor, 'up');
            });
            floorDiv.appendChild(upArrow);
        }

        if (floor > 1) {
            const downArrow = document.createElement('button');
            downArrow.textContent = '↓';
            downArrow.classList.add('arrow', 'down-arrow');
            downArrow.addEventListener('click', () => {
                callElevator(floor, 'down');
            });
            floorDiv.appendChild(downArrow);
        }

        controlDiv.appendChild(floorDiv);
    }
    controlContainer.appendChild(controlDiv);
}

function renderElevators(elevators) {
    const elevatorContainer = document.getElementById('elevator-container');
    elevatorContainer.innerHTML = '';
    elevators.forEach(elevator => {
        const elevatorDiv = document.createElement('div');
        elevatorDiv.classList.add('elevator-column');
        for (let floor = 1; floor <= 10; floor++) {
            const floorDiv = document.createElement('div');
            floorDiv.classList.add('floor');

            if (floor === elevator.current_floor) {
                floorDiv.classList.add('current-floor');
            } else if (elevator.target_floors.includes(floor)) {
                floorDiv.classList.add(elevator.status === 'up' ? 'up' : 'down');
            }

            const floorLabel = document.createElement('div');
            floorLabel.textContent = floor;
            floorLabel.classList.add('floor-label')


            floorLabel.addEventListener('click', () => {
                stopElevator(elevator.id, floor);
            });

            floorDiv.appendChild(floorLabel);
            elevatorDiv.appendChild(floorDiv);
        }

        elevatorContainer.appendChild(elevatorDiv);
    });

    renderControl()
}



function callElevator(floor, direction) {
    fetch('/api/call-elevator/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            floor_number: floor,
            direction: direction
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);

        fetchElevatorData();
    })
    .catch(error => console.error('Error calling elevator:', error));
}


function stopElevator(elevatorId, floor) {
    console.log('click', floor)
    fetch('/api/choose-target-floor/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            elevator_id: elevatorId,
            floor_number: floor
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        fetchElevatorData();
    })
    .catch(error => console.error('Error stopping elevator:', error));
}