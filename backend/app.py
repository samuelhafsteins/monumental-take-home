import math
from flask import Flask
from flask_socketio import SocketIO

from threading import Lock

from helpers import FRAMES
from robot import robot

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

socketio = SocketIO(app, cors_allowed_origins="*")

thread = None
thread_lock = Lock()


@app.route("/test")
def test():
    robot.move(4, 4)
    return "Test"


def send_robot():
    global thread
    while True:
        socketio.sleep(1 / FRAMES)
        socketio.emit("robot", robot.get_robot_data())


@socketio.on("connect")
def handle_connect():
    print("Connected")
    # If we want constant update, uncomment this line
    # global thread
    # with thread_lock:
    #     if thread is None:
    #         thread = socketio.start_background_task(send_robot)


@socketio.on("disconnect")
def handle_disconnect():
    print("Disconnected")


@socketio.on("get_robot")
def handle_get_robot():
    # In case client disconnects
    socketio.emit("robot", robot.get_robot_data())


@socketio.on("robot_move")
def handle_robot_move(x, y):
    robot.move(x, y)
    print(f"Move robot to {x}, {y}")


@socketio.on("robot_rotate_crane")
def handle_robot_rotate_crane(phi):
    # phi received in degrees
    robot.crane.rotate(math.radians(phi))
    print(f"Rotate crane: {phi}")


@socketio.on("robot_move_elbow")
def handle_robot_move_elbow(z):
    # z received in mm
    robot.elbow.move(z / 1000)
    print(f"Lift elbow to {z}")


@socketio.on("robot_rotate_elbow")
def handle_robot_rotate_elbow(phi):
    robot.elbow.rotate(math.radians(phi))
    print(f"Rotate elbow: {phi}")


@socketio.on("robot_rotate_wrist")
def handle_robot_rotate_wrist(phi):
    robot.wrist.rotate(math.radians(phi))
    print(f"Rotate wrist: {phi}")


@socketio.on("robot_gripper")
def handle_robot_gripper(space):
    robot.gripper.move(space)
    print(f"Gripper open to {space}")
