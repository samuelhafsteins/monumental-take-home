from flask import Flask
from flask_socketio import SocketIO

from routes import api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

app.register_blueprint(api, url_prefix="/api")
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("connect")
def handle_connected():
    print("Connected")

@socketio.on("disconnect")
def handle_connected():
    print("Disconnected")

@socketio.on("robot_move")
def handle_robot_move(x, y):
    print(f"Move robot to {x}, {y}")

@socketio.on("robot_swing")
def handle_robot_swing(degrees):
    print(f"Swing {degrees}")

@socketio.on("robot_lift")
def handle_robot_lift(z):
    print(f"Lift to {z}")

@socketio.on("robot_rotate_elbow")
def handle_robot_rotate_elbow(degrees):
    print(f"Rotate elbow {degrees}")

@socketio.on("robot_roate_wrist")
def handle_robot_rotate_wrist(degress):
    print(f"Rotate wrist {degress}")

@socketio.on("robot_gripper")
def handle_robot_gripper(space):
    print(f"Gripper open to {space}")

if __name__ == "__main__":
    socketio.run(app, debug=True)