<script setup lang="ts">
import Scene from './components/Scene/Scene.vue';

import { socket } from './socket';

socket.connect();
fetch("/api/robot").then(res => res.json()).then(data => console.log(data))
</script>

<template>
  <Scene />
</template>

<style scoped>

</style>
