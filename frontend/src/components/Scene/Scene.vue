<script setup lang="ts">
import { onMounted, reactive } from 'vue'
import { init } from './Scene';
import { moveRobot, updateRobot } from '../../socket';
import { RobotData } from '../../models';

const robotData = reactive({x: 0, y: 0} as RobotData)
onMounted(() => {
  init();
  updateRobot()
})
</script>

<template>
  <div id="inputs">
    <div>
      Move Robot <br />
      X: <input v-model="robotData.x"/>
      <br />
      Y: <input v-model="robotData.y"/>
      <br />
      <button @click="() => moveRobot(robotData.x, robotData.y)"> Send to location </button>
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
