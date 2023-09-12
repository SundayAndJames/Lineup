<template>
  <!-- 弹窗 -->
  <FilterCountry :show="showPopup" :allCountries="allCountries" @close-popup="showPopup = false"
    @update="updateFromFilterCountry" />
  <div id="schoolTable">
    <!-- 表格 -->
    <table>
      <!-- 表头 -->
      <thead>
        <!-- 表行 -->
        <tr>
          <!-- 表标题单元格 -->
          <th>
            <div class="thContent">
              Rank
            </div>
            <div class="resizeHandler" @mousedown="resizeCellData.startResize"></div>
          </th>
          <th>
            <div class="thContent">
              School Name
            </div>
            <div class="resizeHandler" @mousedown="resizeCellData.startResize"></div>
          </th>
          <th @mouseenter="showImg = true" @mouseleave="showImg = false">
            <div id="countryButton" style="display: block;" v-if="showImg">
              <img src="/src/assets/filter.jpg" alt="过滤按钮" @click="showPopup = true" />
            </div>
            <div class="thContent">
              Country
            </div>
            <div class="resizeHandler" @mousedown="resizeCellData.startResize"></div>
          </th>
          <th class="attribute" v-for="(attribute, index) in currentAttributes" :key="attribute"
            @mousedown="moveDataAndFunction.startMove(attribute)" @mouseenter="showAttributeButton[attribute] = true"
            @mouseleave="showAttributeButton[attribute] = false">
            <div class="removeButton" style="display: block;" v-if="showAttributeButton[attribute]">
              <img src="/src/assets/removed.png" alt="删除按钮" @click="removeDataAndFunction.removeAttribute(attribute)" />
            </div>
            <div class="movePosition" @mouseup="moveDataAndFunction.getPosition(index)"></div>
            <div class="triangle" v-show="isSorted[attribute]"></div>
            <div class="thContent" @click="selectSortAttribute(attribute, $event)">
              {{ attribute }}
            </div>
            <div class="resizeHandler" @mousedown="resizeCellData.startResize"></div>
          </th>
          <th>
            <div class="thContent">sum</div>
          </th>
        </tr>
      </thead>
      <!-- 表主体 -->
      <tbody>
        <!-- 表行：循环 -->
        <tr v-for="(school, index) in filteredSchools" :key="school.name">
          <!-- 表数据单元格 -->
          <td>{{ index + 1 }}</td>
          <td>{{ school.name }}</td>
          <td>{{ school.country }}</td>
          <!-- <td>{{ school['Academic Reputation'] }}</td> -->
          <td class="percentage-cell" v-for="attrbute in currentAttributes"
            :style="getFillStyle(school[attrbute], attrbute)">
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <!-- 属性仓库，用于存储removed的attribute和需要restore的attribute -->
  <div class="attributesHub">
    <div class="removedAttributes" :style="{ backgroundColor: colors[attribute] }"
      v-for="(attribute, index) in removedAttributes" :key="attribute"
      @mousedown="moveDataAndFunction.startAdd(attribute)">{{ attribute }}</div>
  </div>
</template>

<script setup>
import { ref, toRefs, computed, watch, reactive } from "vue";
import FilterCountry from "./Filters/FilterCountry.vue";
//定义props
const props = defineProps({
  schools: {
    type: Array,
    required: true,
  },
  allCountries: {
    type: Array,
    required: true,
  },
});
//解构props
const { schools, allCountries } = toRefs(props);
//attributes属性列
const attributes = reactive(['Academic Reputation', 'Employer Reputation', 'Faculty Student',
  'Citations per Faculty', 'International Faculty', 'International Students',
  'International Research Network', 'Sustainability'])
const currentAttributes = reactive([...attributes]) //现有属性列
const removedAttributes = reactive([]) //被移除的属性列
//被选择的国家
const selectedCountries = ref([...allCountries.value]);
watch(selectedCountries, (newValue, oldValue) => {
  console.log("现在选中的国家有：", newValue);
  console.log("之前选中的国家有：", oldValue);
});
watch(allCountries, (newValue, oldValue) => {
  console.log("现在所有国家有：", newValue);
  console.log("之前所有国家有：", oldValue);
  selectedCountries.value = [...newValue];
});
//选择排序属性
const sortAttribute = ref('');
const isSorted = reactive({
  'Academic Reputation': false,
  'Employer Reputation': false,
  'Faculty Student': false,
  'Citations per Faculty': false,
  'International Faculty': false,
  'International Students': false,
  'International Research Network': false,
  'Employment Outcomes': false,
  'Sustainability': false,
}); //是否使用某属性进行排序
//选择排序属性
const selectSortAttribute = (attribute, event) => {
  if (isSorted[attribute]) {
    isSorted[attribute] = false;
    sortAttribute.value = '';
  } else {
    //全部设为false，仅保留被点击的属性为true
    Object.keys(isSorted).forEach(key => {
      isSorted[key] = false;
    });
    const elements = document.querySelectorAll('.attribute');
    elements.forEach(element => {
      // 对每一个 element 进行你想要的操作
      element.style.borderColor = "white";
    });
    isSorted[attribute] = true;
    sortAttribute.value = attribute;
  }
}
//定义计算属性
const filteredSchools = computed(() => {
  let data = schools.value.filter((school) =>
    selectedCountries.value.includes(school.country)
  );
  if (sortAttribute.value == '') return data;
  else {
    data = data.sort((a, b) => b[sortAttribute.value] - a[sortAttribute.value])
    return data;
  }
});
//显示弹窗
const showPopup = ref(false);
//显示功能图标
const showImg = ref(false);
//显示属性功能图标
const showAttributeButton = reactive({
  "Academic Reputation": false,
  "Employer Reputation": false,
  "Faculty Student": false,
  "Citations per Faculty": false,
  "International Faculty": false,
  "International Students": false,
  "International Research Network": false,
  "Employment Outcomes": false,
  "Sustainability": false,
})
const colors = {
  "Academic Reputation": "#f08080",
  "Employer Reputation": "#FFA500",
  "Faculty Student": "#80f0e5",
  "Citations per Faculty": "#5bf7b8",
  "International Faculty": "#f56ea4",
  "International Students": "#f7be5b",
  "International Research Network": "#FFC0CB",
  "Employment Outcomes": "#f5876e",
  "Sustainability": "#bab6b6",
};

//填充单元格的颜色
const getFillStyle = (percentage, attribute) => {
  return {
    "--fill-percentage": `${percentage}%`,
    "--color": `${colors[attribute]}`,
  };
};
//过滤后更新selectedCountries
const updateFromFilterCountry = (value) => {
  selectedCountries.value = value;
  console.log(selectedCountries.value);
};
//有关resize的所有属性和方法
const resizeCellData = reactive({
  isResizing: false,  //是否正在调整大小
  startX: null,  //调整时鼠标的初始位置
  startWidth: null, //调整时列的初始宽度
  currentTh: null, //当前被调整的th
  // 当用户点击可拖拽的手柄时，此函数会被调用
  startResize(event) {
    resizeCellData.isResizing = true; // 开始调整大小
    resizeCellData.currentTh = event.target.parentElement;// 获取当前被调整的th元素
    resizeCellData.startX = event.clientX;// 记录开始时的鼠标位置
    resizeCellData.startWidth = resizeCellData.currentTh.offsetWidth;// 记录开始时的列宽度
    // 当鼠标移动或松开时，添加事件监听器以处理这些情况
    document.addEventListener('mousemove', resizeCellData.handleMouseMove);
    document.addEventListener('mouseup', resizeCellData.stopResize);
  },
  // 当用户拖动鼠标时，此函数会被调用
  handleMouseMove(event) {
    if (!resizeCellData.isResizing || !resizeCellData.currentTh) return;
    const diffX = event.clientX - resizeCellData.startX;// 计算鼠标移动的距离
    // 根据鼠标的移动调整列的宽度
    resizeCellData.currentTh.style.width = `${resizeCellData.startWidth + diffX}px`;
    event.preventDefault();
  },
  // 当用户松开鼠标时，此函数会被调用
  stopResize() {
    resizeCellData.isResizing = false;
    // 移除之前添加的事件监听器
    document.removeEventListener('mousemove', resizeCellData.handleMouseMove);
    document.removeEventListener('mouseup', resizeCellData.stopResize);
  }
});
//move attribute相关方法和变量
const moveDataAndFunction = reactive({
  isMoving: false,
  isAdding: false,
  movedAttribute: "", //试图移动的属性
  addedAttribute: "", //试图添加的属性
  startMove: (attrbute) => {
    moveDataAndFunction.isMoving = true;
    moveDataAndFunction.movedAttribute = attrbute;
    document.addEventListener('mouseup', moveDataAndFunction.stopMove);
  },
  startAdd: (attrbute) => {
    moveDataAndFunction.isAdding = true;
    moveDataAndFunction.addedAttribute = attrbute;
    document.addEventListener('mouseup', moveDataAndFunction.stopAdd);
  },
  stopMove: () => {
    moveDataAndFunction.isMoving = false;
    moveDataAndFunction.movedAttribute = "";
    document.removeEventListener('mouseup', moveDataAndFunction.stopMove);
  },
  stopAdd: () => {
    moveDataAndFunction.isAdding = false;
    moveDataAndFunction.addedAttribute = "";
    document.removeEventListener('mouseup', moveDataAndFunction.stopAdd);
  },
  getPosition: (toIndex) => {
    if (moveDataAndFunction.isMoving) {
      const fromIndex = currentAttributes.findIndex(col => col === moveDataAndFunction.movedAttribute)
      const [element] = currentAttributes.splice(fromIndex, 1);
      currentAttributes.splice(toIndex, 0, element);
    }
    if (moveDataAndFunction.isAdding) {
      currentAttributes.splice(toIndex, 0, moveDataAndFunction.addedAttribute);
      const addIndex = removedAttributes.findIndex(col => col === moveDataAndFunction.addedAttribute)
      removedAttributes.splice(addIndex, 1);
    }

  },
})
//remove attribue相关方法和变量
const removeDataAndFunction = reactive({
  removeAttribute: (attrbute) => {
    const removedIndex = currentAttributes.findIndex(col => col === attrbute)
    const [element] = currentAttributes.splice(removedIndex, 1);
    removedAttributes.push(element)
  }
})
</script>

<!-- scoped代表CSS只作用为当前组件 -->
<style scoped>
/* 表格容器 */
#schoolTable {
  height: 90%;
  width: 100%;
  position: relative;
  overflow-x: auto;
  overflow-y: auto;
}

/* 表格自身 */
table {
  position: absolute;
  table-layout: fixed;
  top: 20px;
  font-size: 5px;
}

thead tr {
  background-color: #f0f0f0;
}

/* 表行控制：灰白循环 */
tbody tr:nth-child(odd) {
  background-color: white;
}

tbody tr:nth-child(even) {
  background-color: #f0f0f0;
}

th {
  /* cursor: pointer; */
  position: relative;
  border: 1px solid white;
  transition: border-color 0.3s;
  height: 10px;
  min-height: 10px;
  max-height: 10px;
  width: 50px;
  /* overflow: hidden; */
  text-overflow: ellipsis;
  /* 可选，将文本截断并显示... */
  white-space: nowrap;
  /* 防止文本换行 */
}

th .triangle {
  position: absolute;
  width: 0;
  height: 0;
  top: 0;
  left: 0;
  border-left: 5px solid black;
  /* 这会创建三角形的垂直边 */
  border-bottom: 5px solid transparent;
  /* 这会创建三角形的水平边 */
  border-top: 5px solid black;
  /* 这会创建三角形的斜边，指向右下角 */
  border-right: 5px solid transparent;
  /* 这会创建三角形的斜边，指向右下角 */
  z-index: 3;
}

th:hover {
  /* 当鼠标悬停时的边框颜色 */
  border-color: black !important;
}

th:hover .resizeHandler {
  display: block;
}

/* body单元格定位 */
td {
  position: relative;
  height: 3px;
  width: 50px;
  max-width: 50px;
  min-width: 50px;
  overflow: hidden;
  text-overflow: ellipsis;
  /* 可选，将文本截断并显示... */
  white-space: nowrap;
  /* 防止文本换行 */
  font-size: 3px;
  font-family: "Arial"
}

/* 单元格伪元素，用于填充颜色 */
td.percentage-cell::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: var(--fill-percentage);
  background-color: var(--color);
}

#countryButton {
  cursor: pointer;
  position: absolute;
  width: 100px;
  height: 20px;
  top: -20px;
  left: 0;
  /* background-color: aqua; */
}

#countryButton img {
  position: absolute;
  left: 0;
  bottom: 0;
  height: 20px;
  width: 20px;
}

/* 设置拖拽手柄的样式 */
.resizeHandler {
  position: absolute;
  top: 0;
  right: -6px;
  bottom: 0;
  width: 6px;
  cursor: ew-resize;
  background-color: black;
  display: none;
  z-index: 3;
}

.movePosition {
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  width: 6px;
  background-color: blue;
  z-index: 2;
  opacity: 0;
  transition: opacity 0.3s;
}

.movePosition:hover {
  opacity: 1;
}

.attributesHub {
  /* background-color: blue; */
  width: 100%;
  height: 10%;
  position: relative;
  display: flex;
  flex-direction: row;
}

button {
  position: relative;
  height: 100%;
  width: 10%;
}

.thContent {
  /* position: relative; */
  height: 100%;
  width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  /* cursor: pointer; */
  user-select: none;
  /* 不可选中文字 */
  font-size: 5px;
  font-family: "Arial"
}

.removedAttributes {
  position: relative;
  height: 100%;
  width: 10%;
  user-select: none;
  border: 1px solid white;
  transition: border-color 0.3s;
}

.removedAttributes:hover {
  border-color: black;
}

.removeButton {
  cursor: pointer;
  position: absolute;
  width: 100px;
  height: 20px;
  top: -20px;
  left: 0;
}

.removeButton img {
  position: absolute;
  left: 0;
  bottom: 0;
  height: 20px;
  width: 20px;
}
</style>
