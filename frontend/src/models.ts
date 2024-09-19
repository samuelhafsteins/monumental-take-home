import * as THREE from "three";

export interface RobotData {
  x: number;
  y: number;
  crane: {
    phi: number;
  };
  elbow: {
    phi: number;
    z: number;
  };
  gripper: {
    space: number;
  };
  wrist: {
    phi: number;
  };
}

// TODO add to class
const robotGeometry = new THREE.BoxGeometry(1, 1, 1);
const robotMaterial = new THREE.MeshBasicMaterial({
  color: 0xffffff,
  wireframe: true,
});

export const robot = new THREE.Mesh(robotGeometry, robotMaterial);

const elbowGeometry = new THREE.BoxGeometry(0.5, 0.5, 2);
const elbowMaterial = new THREE.MeshBasicMaterial({
  color: 0xffa500,
  wireframe: true,
});
export const elbow = new THREE.Mesh(elbowGeometry, elbowMaterial);

const wristGeometry = new THREE.BoxGeometry(0.3, 0.3, 2.5);
const wristMaterial = new THREE.MeshBasicMaterial({
  color: 0x0000ff,
  wireframe: true,
});
export const wrist = new THREE.Mesh(wristGeometry, wristMaterial);
