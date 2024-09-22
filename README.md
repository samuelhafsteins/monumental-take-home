# Visualizing a Robotic Crane (Controls)

Take home assignment, apologies in advance if you find the UI a bit raw.

## Run program

### Backend

Start by changing your directory to `backend` and run `pip install -r requirements.txt` (I recomend using a python venv).

To start the backend run `python main.py`, python version used in development is `3.12.6`.

### Fronted

Start by changing your directory to `frontend` and run `npm install`.

To start the frontend run `npm run dev`, the default url should be `http://localhost:5173/`.

## Usage

On the left hand side of the window you have the controls.
With them you can control every moving part of the robot.
In addition you have two extra options:

* An inverse kinematic that will send the robot to a desired postion, while mainting the current rotations on the wrist and elbow.
* A checkbox under the movement section that will tell the robot to keep the gripper still and move to a desired position.
Note that there is no bound check, thus picking a position which the robot could not access while keeping the gripper at the current location will stop the robot.

## Assumptions

I took a few assumptions while writing the assignment, mostly to safe time so that I can focus on creating the robot and the controls.

* I assume the data is always in the correct format when it is sent over the websocket.
* I did not implement any direct bound checks for the sent data.
* To avoid floating point errors when reaching a desired postion, I have a cutoff point for each movement.
* I assumed the stopping time of the robot is minimal, thus it directly stops when it reaches a desired position.
* I allow all rotations to be a full 360 degrees, thus not checking any hitboxes with the robot itself.