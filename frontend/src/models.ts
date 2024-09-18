export interface RobotData {
    x: number;
    y: number;
    crane: {
        phi: number;
        z: number;
    }
    elbow: {
        phi: number;
    }
    gripper: {
        space: number;
    }
    wrist: {
        phi: number;
    }
}
