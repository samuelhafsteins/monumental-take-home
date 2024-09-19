<script setup lang="ts">
import Scene from './components/Scene/Scene.vue';

import { socket } from './socket';
socket.connect();

</script>

<template>
  <Scene />
</template>
