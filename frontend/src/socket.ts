import {io} from "socket.io-client"
import { robot } from "./models";
import { RobotData } from "./models";

export const socket = io('ws://localhost:5000', {autoConnect: false})

export const updateRobot = () => {
    socket.on("robot", (robotData: RobotData) => {
        robot.position.x = robotData.x;
        robot.position.z = robotData.y;
    });
}

export const moveRobot = (x: number, y: number) => {
    socket.emit("robot_move", x, y);
}