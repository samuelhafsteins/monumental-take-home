from threading import Thread, Lock
from time import sleep

from app import socketio, app
from robot import robot
from helpers import FRAMES

thread_lock = Lock()


def robot_loop():
    # Emulated robot loop
    while True:
        if (
            robot.check_move()
            or robot.elbow.check_move()
            or robot.elbow.check_rotate()
            or robot.crane.check_rotate()
            or robot.wrist.check_rotate()
        ):
            socketio.emit("robot", robot.get_robot_data())
        sleep(1 / FRAMES)


if __name__ == "__main__":
    with thread_lock:
        thread = Thread(target=robot_loop)
        thread.start()

    socketio.run(app, debug=True, use_reloader=False)
