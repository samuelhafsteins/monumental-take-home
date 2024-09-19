<script setup lang="ts">
import { robot } from './components/Scene/Scene';
import Scene from './components/Scene/Scene.vue';
import { RobotData } from './models';

import { socket } from './socket';

socket.connect();

socket.on("robot", (robotData: RobotData) => {
  robot.position.x = robotData.x;
  robot.position.z = robotData.y;
});
</script>

<template>
  <Scene />
</template>

<style scoped>

</style>
