<template>
  <RouterView />
</template>









<script setup lang="ts">
</script>






<style scoped>

* {
  box-sizing: border-box; /* 👈 Extrem Wichtig! */
  margin: 0;
  padding: 0;
}

body {
  font-family: Arial, Helvetica, sans-serif; /* Wichtige Schriftart festlegen */
  line-height: 1.5; /* Verbessert die Lesbarkeit */
  background-color: #f8f8f8; /* Hellgrauer Hintergrund (optional) */
  color: #333; /* Dunkelgraue Standard-Textfarbe */
}

#app {
  /* Setzt die minimale Höhe des Haupt-Containers auf die Höhe des Viewports */
  min-height: 100vh; 
  
}

</style>


