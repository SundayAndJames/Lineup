<template>
  <div v-if="show" id="popup">
    <h3>Filter</h3>
    <button @click="selectAll">Select All</button>
    <button @click="deselectAll">Delete All</button>
    <ul>
      <li v-for="country in allCountries" :key="country">
        <input type="checkbox" :value="country" v-model="selectedCountries" />
        {{ country }}
      </li>
    </ul>
    <button @click="Ok">OK</button>
    <button @click="close">Close</button>
  </div>
</template>

<script setup>
import { ref, toRefs, defineEmits } from "vue";
// 定义 props 和 emits
const props = defineProps({
  show: {
    type: Boolean,
    required: true,
  },
  allCountries: {
    type: Array,
    required: true,
  },
});
//自定义事件
const emit = defineEmits(["update", "close-popup"]);
//解构props
const { show, allCountries } = toRefs(props);
const selectedCountries = ref([]);

const selectAll = () => {
  selectedCountries.value = [...allCountries.value];
};

const deselectAll = () => {
  selectedCountries.value = [];
};

const Ok = () => {
  emit("update", selectedCountries.value);
};
const close = () => {
  emit("close-popup");
};
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

#popup ul {
  max-height: 300px;
  /* Adjust this value based on your needs */
  overflow-y: auto;
  /* Show vertical scrollbar if content overflows */
}
</style>
