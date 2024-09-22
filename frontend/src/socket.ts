import { io } from "socket.io-client";
import { Robot } from "./models";
import { RobotData } from "./models";

export const socket = io("ws://localhost:5000", { autoConnect: false });

export const getRobot = () => {
  socket.emit("get_robot");
};

export const updateRobot = (robot: Robot) => {
  socket.on("robot", (robotData: RobotData) => {
    robot.update(robotData);
  });
};

export const moveRobot = (x: string, y: string) => {
  socket.emit("robot_move", parseFloat(x), parseFloat(y));
};

export const liftCrane = (z: string) => {
  socket.emit("robot_lift", parseFloat(z));
};

export const rotateCrane = (phi: string) => {
  socket.emit("robot_rotate_crane", parseFloat(phi));
};

export const rotateElbow = (phi: string) => {
  socket.emit("robot_rotate_elbow", parseFloat(phi));
};

export const rotateWrist = (phi: string) => {
  socket.emit("robot_rotate_wrist", parseFloat(phi));
};

export const openGripper = (space: string) => {
  socket.emit("robot_open_gripper", parseFloat(space));
};
