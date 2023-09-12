<template>
  <div class="container">
    <div class="leftContainer">
      <button @click="addSum">添加SUM</button>
    </div>
    <div id="lineUpContainer">
      <RankTable :ifSum="ifSum" :schools="schoolData" :allCountries="allCountries" @deleteSum="deleteSum" />
    </div>
  </div>
</template>

<script setup>
import RankTable from "./components/RankTable.vue";
import SchoolName from "./components/SchoolName.vue";

import { onMounted, ref } from "vue";

const schoolData = ref([
  // { rank: 1, name: "Harvard University", country: "US" },
  // { rank: 2, name: "Oxford University", country: "UK" },
  // ... other schools
]);

const error = ref(null);
const allCountries = ref([]);
const ifSum = ref(false)
const getData = async () => {
  try {
    const response = await fetch("http://127.0.0.1:5000/getData");
    const val = await response.json();
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    allCountries.value = val[1];
    console.log(allCountries.value);
    schoolData.value = val[0];
  } catch (err) {
    error.value = err.message;
  }
};
const deleteSum = () => {
  ifSum.value = false;
}
const addSum = () => {
  ifSum.value = true
}
onMounted(() => {
  getData();
})
</script>

<style scoped>
.container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
}

.leftContainer {
  width: 150px;
  background-color: antiquewhite;
}

#lineUpContainer {
  display: flex;
  flex-direction: column;
}
</style>