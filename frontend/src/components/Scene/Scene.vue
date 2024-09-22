<script setup lang="ts">
import { onMounted, reactive } from "vue";
import { init } from "./Scene";
import {
  moveRobot,
  updateRobot,
  liftCrane,
  rotateCrane,
  rotateElbow,
  rotateWrist,
  getRobot,
  openGripper,
} from "../../socket";
import { Robot } from "../../models";

const robotData = reactive({
  x: "0",
  z: "0",
  crane: { phi: "0", y: "0" },
  elbow: { phi: "0" },
  wrist: { phi: "0" },
  gripper: { space: "0" },
});

onMounted(() => {
  const robot = new Robot();
  init(robot.getRenders());
  updateRobot(robot);
  getRobot();
});
</script>

<template>
  <div id="inputs">
    <div>
      Move Robot <br />
      X (m): <input v-model="robotData.x" />
      <br />
      Z (m): <input v-model="robotData.z" />
      <br />
      <button @click="() => moveRobot(robotData.x, robotData.z)">
        Send to location
      </button>
    </div>
    <div>
      Lift crane <br />
      Y (mm): <input v-model="robotData.crane.y" />
      <br />
      <button @click="() => liftCrane(robotData.crane.y)">Move elbow</button>
    </div>
    <div>
      Rotate robot <br />
      Degrees: <input v-model="robotData.crane.phi" />
      <br />
      <button @click="() => rotateCrane(robotData.crane.phi)">
        Rotate crane
      </button>
    </div>
    <div>
      Rotate elbow <br />
      Degrees: <input v-model="robotData.elbow.phi" />
      <br />
      <button @click="() => rotateElbow(robotData.elbow.phi)">
        Rotate elbow
      </button>
    </div>
    <div>
      Rotate wrist <br />
      Degrees: <input v-model="robotData.wrist.phi" />
      <br />
      <button @click="() => rotateWrist(robotData.wrist.phi)">
        Rotate wrist
      </button>
    </div>
    <div>
      Open gripper <br />
      Space (mm): <input v-model="robotData.gripper.space" />
      <br />
      <button @click="() => openGripper(robotData.gripper.space)">
        Open gripper
      </button>
    </div>
  </div>
  <canvas id="scene"></canvas>
</template>

<style scoped>
#inputs {
  position: fixed;
  left: 0;
  top: 0;
}
canvas {
  position: fixed;
  top: 0;
  right: 0;
}
</style>
