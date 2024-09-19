from app import socketio

from robot import robot

@socketio.on("robot_move")
def handle_robot_move(x, y):
    robot.move(x, y)
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
    