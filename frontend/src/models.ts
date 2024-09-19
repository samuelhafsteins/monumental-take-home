import * as THREE from "three";
import { ref } from "vue";

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

// TODO add to class
const robotGeometry = new THREE.BoxGeometry(1, 1, 1);
const robotMaterial = new THREE.MeshBasicMaterial({color: 0xFFFFFF, wireframe: true});

export const robot = new THREE.Mesh(robotGeometry, robotMaterial);