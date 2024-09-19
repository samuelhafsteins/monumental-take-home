import { io } from "socket.io-client";
import { elbow, robot, wrist } from "./models";
import { RobotData } from "./models";

export const socket = io("ws://localhost:5000", { autoConnect: false });

export const getRobot = () => {
  socket.emit("get_robot");
};

export const updateRobot = () => {
  socket.on("robot", (robotData: RobotData) => {
    robot.position.x = robotData.x;
    robot.position.z = robotData.y;

    robot.rotation.y = robotData.crane.phi;

    elbow.position.y = robotData.elbow.z;
    elbow.rotation.y = robotData.elbow.phi;

    wrist.rotation.y = robotData.wrist.phi;
  });
};

export const moveRobot = (x: string, y: string) => {
  socket.emit("robot_move", parseFloat(x), parseFloat(y));
};

export const moveElbow = (z: string) => {
  socket.emit("robot_move_elbow", parseFloat(z));
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
