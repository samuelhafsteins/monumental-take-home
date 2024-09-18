<script setup lang="ts">
import { onMounted } from 'vue'
import { init } from './Scene';

onMounted(() => {
  init();
})
</script>

<template>
  <canvas id="scene"></canvas>
</template>

<style scoped>
canvas {
  position: fixed;
  top: 0;
  left: 0; 
}
</style>
