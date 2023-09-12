<template>
  <div ref="draggable" class="draggable" @mousedown="dragStart">
    拖拽我
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue';

const draggable = ref(null);
let startX = 0;
let startY = 0;
let initialLeft = 0;
let initialTop = 0;

const dragStart = (event) => {
  startX = event.clientX;
  startY = event.clientY;
  initialLeft = draggable.value.offsetLeft;
  initialTop = draggable.value.offsetTop;

  document.addEventListener('mousemove', dragMove);
  document.addEventListener('mouseup', dragEnd);
};

const dragMove = (event) => {
  const dx = event.clientX - startX;
  const dy = event.clientY - startY;

  draggable.value.style.left = `${initialLeft + dx}px`;
  draggable.value.style.top = `${initialTop + dy}px`;
};

const dragEnd = () => {
  document.removeEventListener('mousemove', dragMove);
  document.removeEventListener('mouseup', dragEnd);
};

// 在组件卸载时确保移除事件监听，防止内存泄露
onUnmounted(() => {
  document.removeEventListener('mousemove', dragMove);
  document.removeEventListener('mouseup', dragEnd);
});
</script>

<style>
.draggable {
  width: 100px;
  height: 100px;
  background-color: lightblue;
  position: absolute; /* 为了让left和top属性生效，需要设置为absolute或relative */
  cursor: pointer;
}
</style>
