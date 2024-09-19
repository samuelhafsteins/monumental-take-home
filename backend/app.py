from flask import Flask
from flask_socketio import SocketIO

from threading import Lock

from helpers import FRAMES
from robot import robot

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

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
        socketio.emit('robot', robot.get_robot_data())

@socketio.on("connect")
def handle_connected():
    print("Connected")
    # If we want constant update, uncomment this line
    # global thread
    # with thread_lock:
    #     if thread is None:
    #         thread = socketio.start_background_task(send_robot)

@socketio.on("disconnect")
def handle_connected():
    print("Disconnected")


@socketio.on("robot_move")
def handle_robot_move(x, y):
    robot.move(int(x), int(y))
    print(f"Move robot to {x}, {y}")

@socketio.on("robot_move_crane")
def handle_robot_swing(z, phi):
    robot.crane.move(z, phi)
    print(f"Lif: {z}, Swing: {phi}")

@socketio.on("robot_rotate_elbow")
def handle_robot_rotate_elbow(phi):
    robot.elbow.rotate(phi)
    print(f"Rotate elbow {phi}")

@socketio.on("robot_roate_wrist")
def handle_robot_rotate_wrist(phi):
    robot.wrist.rotate(phi)
    print(f"Rotate wrist {phi}")

@socketio.on("robot_gripper")
def handle_robot_gripper(space):
    robot.gripper.move(space)
    print(f"Gripper open to {space}")
