# Elevator system

## How to run this project?

###  Running the application by Docker
 
- Step 1: Clone project
    ```
  git clone git@github.com:HoangNA1911/elevator_system.git
  cd <project folder>
    ```
- Step 2: Build the docker image
  ```
  docker build -t elevator_system .
  ```
- Step 3: Run the Docker Container
  ```
  docker run -p 8000:8000 elevator_system
  ```

### Running the application locally 

- Step 1: Clone project
    ```
  git clone git@github.com:HoangNA1911/elevator_system.git
  cd <project folder>
    ```
- Step 2: Set Up a Virtual Environment (Optional)
  ```
  python -m venv venv
  source venv/bin/activate
  ```
- Step 3: Install Dependencies
  ```
  pip install -r requirements.txt
  ```
- Step 4: Apply Database Migrations
  ```
  python manage.py migrate
  ```
- Step 5: Run the Development Server
  ```
  python manage.py runserver
  ```

## description of elevator system

The system will calculate and determine the best elevator based on travel distance, the current location of each elevator, and the floor request location to optimize energy efficiency and save time.

In this system, the elevator class will include the following information:

- current_floor: represents the current floor of the elevator,
- status: the current status of the elevator (up, down, idle),
- direction: the request direction, meaning the elevator can only stop for requests moving in the same direction,
- target_floor: a list of floors where the elevator needs to stop,
- is_open: indicates the door state (open or closed).