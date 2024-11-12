document.addEventListener("DOMContentLoaded", () => {
    moveAndFetchElevatorData();
    setInterval(moveAndFetchElevatorData, 2000);
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
    fetch('/elevator/')
        .then(response => response.json())
        .then(data => renderElevators(data))
        .catch(error => console.error('Error fetching elevator data:', error));
}

function renderElevators(elevators) {
    const elevatorsDiv = document.getElementById('elevators');
    const floorControls = document.getElementById('floor-controls');

    elevatorsDiv.innerHTML = ''; // Xóa dữ liệu thang máy cũ
    floorControls.innerHTML = ''; // Xóa dữ liệu nút bấm tầng cũ

    elevators.forEach(elevator => {
        const elevatorDiv = document.createElement('div');
        elevatorDiv.classList.add('elevator');

        // Tạo các tầng từ tầng 10 xuống tầng 1 (để phù hợp với giao diện từ trên xuống)
        for (let floor = 10; floor >= 1; floor--) {
            const floorDiv = document.createElement('div');
            floorDiv.classList.add('floor');

            // Thêm các lớp cho tầng hiện tại hoặc tầng có yêu cầu
            if (floor === elevator.current_floor) {
                floorDiv.classList.add('current-floor');
            } else if (elevator.target_floors.includes(floor)) {
                floorDiv.classList.add(elevator.status === 'up' ? 'up' : 'down');
            }

            // Nhãn hiển thị số tầng
            const floorLabel = document.createElement('span');
            floorLabel.textContent = floor;
            floorDiv.appendChild(floorLabel);

            // Nút mũi tên lên (nếu không phải tầng trên cùng)
            if (floor < 10) {
                const upArrow = document.createElement('button');
                upArrow.textContent = '↑';
                upArrow.classList.add('arrow', 'up-arrow');
                upArrow.addEventListener('click', () => {
                    callElevator(elevator.id, floor, 'up');
                });
                floorDiv.appendChild(upArrow);
            }

            // Nút mũi tên xuống (nếu không phải tầng trệt)
            if (floor > 1) {
                const downArrow = document.createElement('button');
                downArrow.textContent = '↓';
                downArrow.classList.add('arrow', 'down-arrow');
                downArrow.addEventListener('click', () => {
                    callElevator(elevator.id, floor, 'down');
                });
                floorDiv.appendChild(downArrow);
            }

            elevatorDiv.appendChild(floorDiv);
        }

        elevatorContainer.appendChild(elevatorDiv);
    });
}


function callElevator(elevatorId, floor, direction) {
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
        console.log(data.message); // Show API response message

        fetchElevatorData();
    })
    .catch(error => console.error('Error stopping elevator:', error));
}
