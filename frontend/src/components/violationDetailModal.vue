<script setup>
import { defineProps, defineEmits } from 'vue';

defineProps({
  anzeigen: Boolean
});

const emit = defineEmits(['close']); 
</script>

<template>
  <Transition name="fade">
    <div v-if="anzeigen" class="modal-hintergrund" @click="$emit('close')">
      <div class="modal-content" @click.stop>
        
        <div class="modal-header">
          <h3><slot name="header">Detail View</slot></h3>
          <button class="close-btn" @click="$emit('close')">×</button>
        </div>

        <div class="modal-body">
          <slot>test</slot>
        </div>

      </div>
    </div>
  </Transition>
</template>

<style scoped>

.modal-hintergrund {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); 
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 1400px;
  max-width: 90%;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>