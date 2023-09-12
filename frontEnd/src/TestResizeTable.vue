<template>
  <table ref="tableRef" border="1">
    <thead>
      <tr>
        <!-- 使用 v-for 循环遍历每个列头，并添加一个可拖拽的手柄 -->
        <th class="resizable" v-for="header in headers" :key="header">
          {{ header }}
          <!-- 当按下此手柄时，开始调整大小的过程 -->
          <div class="resize-handle" @mousedown="startResize($event)"></div>
        </th>
      </tr>
    </thead>
    <tbody>
      <!-- 表格内容 -->
      <tr>
        <td>1</td>
        <td>浙江大学</td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

// ref用于绑定到DOM元素，使我们可以在JS中访问它
const tableRef = ref(null);

// 初始化一些需要的变量
let isResizing = ref(false); // 是否正在调整大小
let startX = ref(0);         // 开始调整大小时的鼠标位置
let startWidth = ref(0);    // 被调整的列的初始宽度
let currentTh = ref(null);  // 当前正在被调整的th元素
const headers = ['Rank', 'School Name']; // 列头数组

// 当用户点击可拖拽的手柄时，此函数会被调用
function startResize(event) {
  isResizing.value = true; // 开始调整大小
  currentTh.value = event.target.parentElement; // 获取当前被调整的th元素
  startX.value = event.clientX; // 记录开始时的鼠标位置
  startWidth.value = currentTh.value.offsetWidth; // 记录开始时的列宽度
  // 当鼠标移动或松开时，添加事件监听器以处理这些情况
  document.addEventListener('mousemove', handleMouseMove);
  document.addEventListener('mouseup', stopResize);
}

// 当用户拖动鼠标时，此函数会被调用
function handleMouseMove(event) {
  if (!isResizing.value || !currentTh.value) return;
  const diffX = event.clientX - startX.value; // 计算鼠标移动的距离
  // 根据鼠标的移动调整列的宽度
  currentTh.value.style.width = `${startWidth.value + diffX}px`;
}

// 当用户松开鼠标时，此函数会被调用
function stopResize() {
  isResizing.value = false; // 停止调整大小
  // 移除之前添加的事件监听器
  document.removeEventListener('mousemove', handleMouseMove);
  document.removeEventListener('mouseup', stopResize);
}

// 当组件挂载时，执行的代码
onMounted(() => {
  // 这里可以添加在组件挂载后需要执行的代码
});

// 在组件卸载之前，执行的代码
onBeforeUnmount(() => {
  // 清除事件监听器，防止内存泄露
  document.removeEventListener('mousemove', handleMouseMove);
  document.removeEventListener('mouseup', stopResize);
});
</script>

<style>
/* 设置列头为可拖拽 */
.resizable {
  position: relative;
}


/* 设置拖拽手柄的样式 */
.resize-handle {
  position: absolute;
  top: 0;
  right: -3px;
  bottom: 0;
  width: 6px;
  cursor: ew-resize;
  background-color: aqua;
}
</style>
