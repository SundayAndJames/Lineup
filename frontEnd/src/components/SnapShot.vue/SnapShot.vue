<template>
  <div class="thead">
    <div class="tr" style="background-color: #f0f0f0;">
      <div class="th" id="seperator">Seperator</div>
      <div class="snapShotAttributes">
        <div class="head" @mouseenter="showButtonImg = true" @mouseleave="showButtonImg = false">
          snapShot
          <img src="/src/assets/removed.png" alt="删除按钮" v-show="showButtonImg" @click="removeSnapShot">
        </div>
        <div class="th">Rank</div>
        <div class="th" v-for="(attribute) in attributes" :key="attribute"
          :style="{ width: `${attributeWidth[attribute]}px`, backgroundColor: headColors[attribute] }">
          {{ attribute }}
          <div class="weightNum">{{ weight[attribute] }}</div>
        </div>
      </div>
    </div>
  </div>
  <div class="tbody">
    <div class="tr" v-for="(data, index) in datas" :key="data.name">
      <div class="seperator" style="position: relative;height: 100%;border: 1px white solid;"></div>
      <div class="td" style="position: relative;height: 100%;border: 1px white solid;">
        {{ index + 1 }}
      </div>
      <div class="td" v-for="(attribute) in attributes" :key="attribute"
        style="position: relative;height: 100%;border: 1px white solid;"
        :style="{ backgroundColor: colors[attribute], width: `${attributeWidth[attribute] * data[attribute] / 100}px` }">
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, toRefs, defineEmits, reactive, watch, computed } from "vue";
const props = defineProps({
  index: {
    type: Number,
    required: true,
  },
  attributes: {
    type: Array,
    required: true,
  },
  datas: {
    type: Array,
    required: true,
  },
  attributeWidth: {
    type: Object,
    required: true,
  },
  weight: {
    type: Object,
    required: true,
  }
});
const { index, attributes, datas, attributeWidth, weight } = toRefs(props);
const colors = {
  "Academic Reputation": "rgb(240,128,128)",
  "Employer Reputation": "rgb(255,165,0)",
  "Faculty Student": "rgb(128,240,229)",
  "Citations per Faculty": "rgb(91,247,184)",
  "International Faculty": "rgb(245,110,164)",
  "International Students": "rgb(247,190,91)",
  "International Research Network": "rgb(255,192,200)",
  "Employment Outcomes": "rgb(245,135,110)",
  "Sustainability": "rgb(186,182,182)",
};
const headColors = {
  "Academic Reputation": "rgb(250,212,212)",
  "Employer Reputation": "rgb(255,225,170)",
  "Faculty Student": "rgb(212,250,246)",
  "Citations per Faculty": "rgb(200,252,231)",
  "International Faculty": "rgb(251,206,224)",
  "International Students": "rgb(252,233,200)",
  "International Research Network": "rgb(255,234,236)",
  "Employment Outcomes": "rgb(251,215,206)",
  "Sustainability": "rgb(232,230,230)",
}
const showButtonImg = ref(false)
const emit = defineEmits(["removeSnapShot"])
const removeSnapShot = () => {
  emit("removeSnapShot", index)
}
</script>

<style scoped>
.head {
  position: absolute;
  top: -40px;
  width: 100%;
  background-color: #f0f0f0;
  border: 1px solid white;
  transition: border-color 0.3s;
  text-align: center;
}

.tbody {
  position: relative;
  display: flex;
  flex-direction: column;
}

.tr {
  position: relative;
  display: flex;
  flex-direction: row;
  height: 20px;
}

/* 表行控制：灰白循环 */
.tr:nth-child(odd) {
  background-color: white;
}

.tr:nth-child(even) {
  background-color: #f0f0f0;
}

.thead .tr {
  height: 80px;
}

.th {
  position: relative;
  height: 100%;
  width: 40px;
  border: 1px white solid;
}

.td {
  position: relative;
  width: 40px;
}

#seperator {
  width: 60px
}

.seperator {
  position: relative;
  width: 60px;
}

.snapShotAttributes {
  position: relative;
  display: flex;
  flex-direction: row;
}

.weightNum {
  position: absolute;
  top: -20px;
  left: 40%;
}

img {
  position: absolute;
  top: -20px;
  left: 0;
  width: 20px;
  height: 20px;
}
</style>