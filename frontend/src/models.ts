import * as THREE from "three";

export interface RobotData {
  x: number;
  z: number;
  crane: {
    phi: number;
    y: number;
  };
  elbow: {
    phi: number;
  };
  wrist: {
    phi: number;
  };
  gripper: {
    space: number;
  };
}

const robotGeometry = new THREE.BoxGeometry(1, 3, 1);
const robotMaterial = new THREE.MeshBasicMaterial({
  color: 0xffffff,
  wireframe: true,
});

const upperARmGeometry = new THREE.BoxGeometry(0.3, 0.3, 2);
const upperArmMaterial = new THREE.MeshBasicMaterial({
  color: 0xffa500,
  wireframe: true,
});

// const elbowWristJointGeometry = new THREE.CylinderGeometry(0.05, 0.05, 0.5);
// const elbowWristJointMaterial = new THREE.MeshBasicMaterial({
//   color: 0xff0000,
//   wireframe: true,
// });
// export const elbowWristJoint = new THREE.Mesh(
//   elbowWristJointGeometry,
//   elbowWristJointMaterial,
// );

const lowerArmGeometry = new THREE.BoxGeometry(0.2, 0.2, 2);
const lowerArmMaterial = new THREE.MeshBasicMaterial({
  color: 0x0000ff,
  wireframe: true,
});

// const wristgripperJointGeometry = new THREE.CylinderGeometry(0.05, 0.05, 0.5);
// const wristgripperJointMaterial = new THREE.MeshBasicMaterial({
//   color: 0xff0000,
//   wireframe: true,
// });
// export const wristgripperJoint = new THREE.Mesh(
//   wristgripperJointGeometry,
//   wristgripperJointMaterial,
// );

const handGeometry = new THREE.BoxGeometry(0.3, 0.5, 0.3);
const handMaterial = new THREE.MeshBasicMaterial({
  color: 0x00ff00,
  wireframe: true,
});

const gripperGeometry = new THREE.BoxGeometry(0.3, 0.1, 0.01);
const gripperMaterial = new THREE.MeshBasicMaterial({
  color: 0x00ffff,
  wireframe: true,
});

export class Robot {
  robot: THREE.Mesh;
  upperArm: THREE.Mesh;
  lowerArm: THREE.Mesh;
  hand: THREE.Mesh;

  gripper: [THREE.Mesh, THREE.Mesh];

  wrist: THREE.Group;
  elbow: THREE.Group;
  arm: THREE.Group;
  robotGroup: THREE.Group;

  constructor() {
    this.robot = new THREE.Mesh(robotGeometry, robotMaterial);
    this.robot.position.y = 1.5;

    this.upperArm = new THREE.Mesh(upperARmGeometry, upperArmMaterial);
    this.lowerArm = new THREE.Mesh(lowerArmGeometry, lowerArmMaterial);
    this.hand = new THREE.Mesh(handGeometry, handMaterial);
    this.gripper = [
      new THREE.Mesh(gripperGeometry, gripperMaterial),
      new THREE.Mesh(gripperGeometry, gripperMaterial),
    ];

    this.gripper[0].translateY(-0.5);
    this.gripper[1].translateY(-0.5);

    this.hand.translateY(-0.2);

    this.wrist = new THREE.Group();
    this.wrist.add(this.hand, ...this.gripper);

    this.wrist.translateZ(2);
    this.wrist.translateY(-0.2);

    this.elbow = new THREE.Group();
    this.elbow.add(this.wrist, this.lowerArm);

    this.lowerArm.translateZ(1);

    this.elbow.translateZ(1);
    this.elbow.translateY(-0.3);

    this.arm = new THREE.Group();
    this.arm.add(this.elbow, this.upperArm);

    this.arm.translateZ(1.5);

    this.robotGroup = new THREE.Group();
    this.robotGroup.add(this.robot, this.arm);
  }

  update(robotData: RobotData): void {
    this.robotGroup.position.set(robotData.x, 0, robotData.z);
    this.robotGroup.rotation.y = robotData.crane.phi;

    this.arm.position.y = robotData.crane.y;

    this.elbow.rotation.y = robotData.elbow.phi;

    this.wrist.rotation.y = robotData.wrist.phi;

    this.gripper[0].position.z = robotData.gripper.space / 2;
    this.gripper[1].position.z = -robotData.gripper.space / 2;
  }

  getRenders(): (THREE.Group | THREE.Mesh)[] {
    return [this.robotGroup];
  }
}
