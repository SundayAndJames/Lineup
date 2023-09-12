<template>
  <div v-if="show" id="popup">
    <h3>WeightSettings</h3>
    <ul>
      <li v-for="attribute in attributes" :key="attribute">
        {{ attribute }}
        <input type="text" maxlength="4" v-model="currentWeight[attribute]" />
      </li>
      <li> totalWeight {{ totalWeight }}</li>
    </ul>
    <button @click="Ok">OK</button>
    <button @click="closePage">Close</button>
  </div>
</template>

<script setup>
import { ref, toRefs, defineEmits, reactive, watch, computed } from "vue";
// 定义 props 和 emits
const props = defineProps({
  show: {
    type: Boolean,
    required: true,
  },
  attributes: {
    type: Array,
    required: true,
  },
  originWeight: {
    type: Object,
    required: true,
  },
  originWidth: {
    type: Object,
    required: true,
  }
});
//自定义事件
const emit = defineEmits(["update", "close"]);
const { show, attributes, originWeight, originWidth } = toRefs(props);
const closePage = () => {
  emit("close")
}
const Ok = () => {
  let totalWidth = 0
  let sumWeight = 0
  for (let key in originWidth.value) {
    totalWidth += Number(originWidth.value[key])
  }
  for (let key in currentWeight) {
    sumWeight += Number(currentWeight[key])
  }
  if (sumWeight !== 1) {
    alert("权重之和必须为1.00")
    return
  }
  for (let key in currentWeight) {
    currentWidth[key] = Number(currentWeight[key]) * totalWidth
    // console.log(currentWidth[key])
  }
  emit("update", currentWeight, currentWidth)
}
const currentWeight = reactive({ ...originWeight.value })
const currentWidth = reactive({ ...originWidth.value })
watch(originWeight, (newVal) => {
  for (let key in newVal) {
    currentWeight[key] = newVal[key]
  }
}, { deep: true });
const totalWeight = computed(() => {
  let total = 0
  for (let key in currentWeight) {
    total += Number(currentWeight[key])
  }
  return total.toFixed(2)
})
</script>

<style scoped>
#popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0px 4px 16px rgba(0, 0, 0, 0.1);
  width: 500px;
  height: 500px;
}
</style>