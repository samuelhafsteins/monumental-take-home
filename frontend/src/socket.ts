import { io } from "socket.io-client";
import { Robot } from "./models";
import { RobotData } from "./models";
import { Ref } from "vue";

export const socket = io("ws://localhost:5000", { autoConnect: false });

export const getRobot = () => {
  socket.emit("get_robot");
};

export const updateRobot = (
  robot: Robot,
  displayData: Ref<RobotData | undefined>,
) => {
  socket.on("robot", (robotData: RobotData) => {
    robot.update(robotData);
    displayData.value = robotData;
  });
};

export const moveRobot = (x: string, y: string, efStill: string) => {
  socket.emit(
    "robot_move",
    parseFloat(x),
    parseFloat(y),
    parseInt(efStill) || false,
  );
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

export const inverseKinematic = (x: string, y: string, z: string) => {
  socket.emit(
    "robot_inverse_kinematic",
    parseFloat(x),
    parseFloat(y),
    parseFloat(z),
  );
};
