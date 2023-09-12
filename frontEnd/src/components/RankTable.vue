<template>
  <div class="functionButton">
    <button @click="snapShotDataAndFuncuton.createSnapShot">snapShot</button>
  </div>
  <!-- 过滤弹窗 -->
  <FilterCountry :show="showFilter" :allCountries="allCountries" @close-popup="showFilter = false"
    @update="updateFromFilterCountry" />
  <!-- 权重调整弹窗 -->
  <WeightSettings :show="showWeightSetting" :attributes="SumDataAndFunction.sumAttributes" :originWeight="weight"
    :originWidth="attributeWidth" @close="showWeightSetting = false" @update="updateWeightAndWidth" />
  <div id="ranktable">
    <div class="table">
      <div class="thead">
        <div class="tr" style="background-color: #f0f0f0;">
          <div class="th Rank" style="background-color: ;">
            <div class="thContent">Rank</div>
            <div class="resizeHandler" @mousedown="resizeCellData.startResize($event, 'Rank')"></div>
          </div>
          <div class="th SchoolName">
            <div class="thContent">School Name</div>
            <div class="resizeHandler" @mousedown="resizeCellData.startResize($event, 'SchoolName')"></div>
          </div>
          <div class="th Country" @mouseenter="showImg = true" @mouseleave="showImg = false">
            <div class="Button" style="display: block;" v-if="showImg">
              <img src="/src/assets/filter.jpg" alt="过滤按钮" @click="showFilter = true" />
            </div>
            <div class="thContent">Country</div>
            <div class="resizeHandler" @mousedown="resizeCellData.startResize($event, 'Country')"></div>
            <div class="movePosition" v-if="currentAttributes.length == 0"
              @mouseup="moveDataAndFunction.finishAddOrMove(0)">
            </div>
          </div>
          <div class="th" :class="[attribute.replace(/\s+/g, '')]" v-for="(attribute, index) in currentAttributes"
            :style="{ backgroundColor: headColors[attribute] }" :key="attribute"
            @mousedown="moveDataAndFunction.startMove(attribute)" @mouseenter="showAttributeButton[attribute] = true"
            @mouseleave="showAttributeButton[attribute] = false">
            <div class="Button" style="display: block;" v-if="showAttributeButton[attribute]">
              <img src="/src/assets/removed.png" alt="删除按钮" @click="removeDataAndFunction.removeAttribute(attribute)" />
            </div>
            <div class="movePosition" v-show="!resizeCellData.isResizing"
              @mouseup="moveDataAndFunction.finishAddOrMove(index)"></div>
            <div class="triangle" v-show="isSorted[attribute]"></div>
            <div class="thContent" @click="selectSortAttribute(attribute, $event)" style="height: 100%;">
              {{ attribute }}
            </div>
            <div class="resizeHandler" @mousedown="resizeCellData.startResize($event, attribute)">
            </div>
          </div>
          <div class="mutiAttributeSum" v-if="ifSum" @mouseenter="SumDataAndFunction.ifShowRemoved = true"
            @mouseleave="SumDataAndFunction.ifShowRemoved = false">
            <div class="Button" v-show="SumDataAndFunction.ifShowRemoved">
              <img src="/src/assets/removed.png" alt="删除按钮" @click="SumDataAndFunction.removeSum" />
            </div>
            <div class="thContent" id="sum" @mouseup="moveDataAndFunction.finishSum"
              @click="selectSortAttribute('sum', $event)">
              <div class="triangle" v-show="isSorted['sum']"></div>
              sum
            </div>
            <div id="attributeContainer">
              <div class="sumAttribute" :class="[attribute.replace(/\s+/g, '')]"
                :style="{ width: `${attributeWidth[attribute]}px` }" v-for="attribute in SumDataAndFunction.sumAttributes"
                :key="attribute" @mouseenter="showAttributeButton[attribute] = true"
                @mouseleave="showAttributeButton[attribute] = false">
                <div class="thContent" style="height: 100%;" :style="{ backgroundColor: headColors[attribute] }">
                  {{ attribute }}
                </div>
                <div class="Button" style="display: block;">
                  <img src="/src/assets/removed.png" alt="删除按钮" @click="SumDataAndFunction.deleteFromSum(attribute)"
                    v-if="showAttributeButton[attribute]" />
                  <div class="weightNum" @click="showWeightSetting = true">{{ weight[attribute] }}</div>
                </div>
                <div class="resizeHandler" @mousedown="resizeCellData.startResize($event, attribute)"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="tbody">
        <div class="tr" v-for="(school, index) in filteredSchools" :key="school">
          <div class="td Rank">{{ index + 1 }}</div>
          <div class="td SchoolName">{{ school.name }}</div>
          <div class="td Country">{{ school.country }}</div>
          <div class="td percentage-cell" :class="[attribute.replace(/\s+/g, '')]" v-for="attribute in currentAttributes"
            :key="attribute" :style="getFillStyle(school[attribute], attribute)">
          </div>
          <div class="sumScore" v-for="(attribute) in SumDataAndFunction.sumAttributes" :key="attribute"
            style="position: relative;height: 100%;border: 1px white solid;"
            :style="{ backgroundColor: colors[attribute], width: `${attributeWidth[attribute] * school[attribute] / 100}px` }">
          </div>
        </div>
      </div>
    </div>
    <div class="snapShots">
      <div class="snapShot" v-for="(snap, index) in snapShotDataAndFuncuton.snapShotArray">
        <SnapShot :attributes="snap.snapShotAttributes" :datas="snap.datas" :attributeWidth="snap.snapShotAttributeWidth"
          :weight="snap.snapShotWeight" :index="index" @removeSnapShot="snapShotDataAndFuncuton.remove" />
      </div>
    </div>
  </div>
  <!-- 属性仓库，用于存储removed的attribute和需要restore的attribute -->
  <div class="attributesHub">
    <div class="removedAttributes" :style="{ backgroundColor: colors[attribute] }"
      v-for="(attribute, index) in removedAttributes" :key="attribute"
      @mousedown="moveDataAndFunction.startAdd(attribute)">{{ attribute }}</div>
  </div>
</template>

<script setup>
import { ref, toRefs, computed, watch, reactive, onMounted } from "vue";
import FilterCountry from "./Filters/FilterCountry.vue";
import WeightSettings from "./WeightSettings/WeightSettings.vue"
import SnapShot from "./SnapShot.vue/SnapShot.vue";
//自定义事件
const emit = defineEmits(['deleteSum']);
//定义props
const props = defineProps({
  ifSum: {
    type: Boolean,
    required: true,
  },
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
const { ifSum, schools, allCountries } = toRefs(props);
//attributes属性列
const attributes = reactive(['Academic Reputation', 'Employer Reputation', 'Faculty Student',
  'Citations per Faculty', 'International Faculty', 'International Students',
  'International Research Network', 'Employment Outcomes', 'Sustainability'])
const currentAttributes = reactive([...attributes]) //现有属性列
const removedAttributes = reactive([]) //被移除的属性列
//被选择的国家
const selectedCountries = ref([...allCountries.value]);
watch(selectedCountries, (newValue, oldValue) => {
  // console.log("现在选中的国家有：", newValue);
  // console.log("之前选中的国家有：", oldValue);
});
watch(allCountries, (newValue, oldValue) => {
  // console.log("现在所有国家有：", newValue);
  // console.log("之前所有国家有：", oldValue);
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
  'sum': false
}); //是否使用某属性进行排序
//选择排序属性
const selectSortAttribute = (attribute, event) => {
  if (isSorted[attribute]) {
    isSorted[attribute] = false;
    sortAttribute.value = '';
  } else if (attribute == 'sum') {
    Object.keys(isSorted).forEach(key => {
      isSorted[key] = false;
    });
    isSorted[attribute] = true;
    sortAttribute.value = attribute;
  }
  else {
    //全部设为false，仅保留被点击的属性为true
    Object.keys(isSorted).forEach(key => {
      isSorted[key] = false;
    });
    const elements = document.querySelectorAll('.attribute');
    elements.forEach(element => {
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
  if (sortAttribute.value == '');
  else if (sortAttribute.value == 'sum') {
    data = data.sort((a, b) => {
      let score1 = 0
      let score2 = 0
      for (let key in weight) {
        score1 += weight[key] * a[key]
        score2 += weight[key] * b[key]
      }
      return (score2 - score1)
    })
  }
  else {
    data = data.sort((a, b) => b[sortAttribute.value] - a[sortAttribute.value])
  }
  return data;
});
//显示过滤弹窗
const showFilter = ref(false);
//显示设置权重弹窗
const showWeightSetting = ref(false)
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
//权重
const weight = reactive({
  'Academic Reputation': 0,
  'Employer Reputation': 0,
  'Faculty Student': 0,
  'Citations per Faculty': 0,
  'International Faculty': 0,
  'International Students': 0,
  'International Research Network': 0,
  'Employment Outcomes': 0,
  'Sustainability': 0,
})
//宽度
const attributeWidth = reactive({
  'Academic Reputation': 0,
  'Employer Reputation': 0,
  'Faculty Student': 0,
  'Citations per Faculty': 0,
  'International Faculty': 0,
  'International Students': 0,
  'International Research Network': 0,
  'Employment Outcomes': 0,
  'Sustainability': 0,
})
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
//设置好权重后更新属性权重和宽度
const updateWeightAndWidth = (updatedWeight, updatedWidth) => {
  for (let key in updatedWeight) {
    weight[key] = updatedWeight[key]
  }
  for (let key in updatedWidth) {
    attributeWidth[key] = updatedWidth[key]
  }
}
//有关resize的所有属性和方法
const resizeCellData = reactive({
  isResizing: false,  //是否正在调整大小
  startX: null,  //调整时鼠标的初始位置
  startWidth: null, //调整时列的初始宽度
  currentTh: null, //当前被调整的th
  currentClass: null,//当前被调整的类
  currentAttribute: null,//当前被调整的属性
  // 当用户点击可拖拽的手柄时，此函数会被调用
  startResize(event, attribute) {
    resizeCellData.currentClass = attribute.replace(/\s+/g, '');
    resizeCellData.currentAttribute = attribute
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
    const width = resizeCellData.startWidth + diffX
    attributeWidth[resizeCellData.currentAttribute] = width
    // 根据鼠标的移动调整列的宽度
    const elements = document.querySelectorAll(`.${resizeCellData.currentClass}`);
    elements.forEach(element => {
      element.style.width = `${width}px`;
    });
    let totalWidth = 0
    for (let key in attributeWidth) {
      totalWidth += attributeWidth[key]
    }
    for (let key in attributeWidth) {
      weight[key] = (attributeWidth[key] / totalWidth).toFixed(2);
    }
    event.preventDefault();//阻止默认事件
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
  isMoving: false, //是否正在移动属性
  isAdding: false, //是否正在添加属性
  isSuming: false, //是否正在添加入sum
  movedAttribute: "", //试图移动的属性
  addedAttribute: "", //试图添加的属性

  startMove: (attribute) => {
    moveDataAndFunction.isMoving = true;
    moveDataAndFunction.movedAttribute = attribute;
    document.addEventListener('mouseup', moveDataAndFunction.stopMove);
  },
  startAdd: (attribute) => {
    moveDataAndFunction.isAdding = true;
    moveDataAndFunction.addedAttribute = attribute;
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
  finishAddOrMove: (toIndex) => {
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
  finishSum: () => {
    if (moveDataAndFunction.isMoving) {
      SumDataAndFunction.sumAttributes.push(moveDataAndFunction.movedAttribute)
      const removedIndex = currentAttributes.findIndex(col => col == moveDataAndFunction.movedAttribute)
      currentAttributes.splice(removedIndex, 1);
      attributeWidth[moveDataAndFunction.movedAttribute] = 80
      // console.log(SumDataAndFunction.sumAttributes)
      let totalWidth = 0
      for (let key in attributeWidth) {
        totalWidth += attributeWidth[key]
      }
      for (let key in attributeWidth) {
        weight[key] = (attributeWidth[key] / totalWidth).toFixed(2);
      }
    }
  }
})
//remove attribue相关方法和变量
const removeDataAndFunction = reactive({
  removeAttribute: (attribute) => {
    const removedIndex = currentAttributes.findIndex(col => col == attribute)
    const [element] = currentAttributes.splice(removedIndex, 1);
    removedAttributes.push(element)
  }
})
//sum相关的方法和变量
const SumDataAndFunction = reactive({
  ifShowRemoved: false,
  addedAttribute: "", //试图添加的属性
  sumAttributes: [], //加入sum的Attribute数组
  removeSum: () => {
    emit("deleteSum");
  },
  deleteFromSum: (attribute) => {
    const removedIndex = SumDataAndFunction.sumAttributes.findIndex(col => col == attribute)
    const [element] = SumDataAndFunction.sumAttributes.splice(removedIndex, 1);
    currentAttributes.push(element)
    showAttributeButton[attribute] = false
    attributeWidth[attribute] = 0
    let totalWidth = 0
    for (let key in attributeWidth) {
      totalWidth += attributeWidth[key]
    }
    for (let key in attributeWidth) {
      weight[key] = (attributeWidth[key] / totalWidth).toFixed(2);
    }
  },
})
//snapShot相关的变量和方法
const snapShotDataAndFuncuton = reactive({
  snapShotArray: [],
  datas: [],
  snapShotAttributes: [],
  snapShotAttributeWidth: {},
  createSnapShot: () => {
    let snap = {}
    snap.datas = [...filteredSchools.value]
    snap.snapShotAttributes = [...SumDataAndFunction.sumAttributes]
    snap.snapShotAttributeWidth = { ...attributeWidth }
    snap.snapShotWeight = { ...weight }
    snapShotDataAndFuncuton.snapShotArray.push(snap)
  },
  remove: (index) => {
    snapShotDataAndFuncuton.snapShotArray.splice(index, 1)
  }
})
</script>


<style scoped>
/*******************************************  thead部分 */
#ranktable {
  height: 90%;
  width: 100%;
  position: relative;
  overflow-x: auto;
  overflow-y: auto;
  display: flex;
  flex-direction: row;
}

/* 表格 */
.table {
  position: relative;
  top: 60px;
  font-size: 5px;
  display: flex;
  flex-direction: column;
}

/* 表头 */
.thead {
  position: relative;
  display: flex;
  flex-direction: row;
}

/* 表头单元格 */
.th {
  /* cursor: pointer; */
  position: relative;
  border: 1px solid white;
  transition: border-color 0.3s;
  height: 80px;
  width: 80px;
}

.thead .tr {
  /* position: relative; */
  height: 80px;
}

/* 表头单元格内容 */
.thContent {
  position: relative;
  /* height: 100%; */
  overflow: hidden;
  /* 可选，将文本截断并显示... */
  text-overflow: ellipsis;
  /* 防止文本换行 */
  white-space: nowrap;
  /* 不可选中文字 */
  user-select: none;
}

/* 小三角 */
.triangle {
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

/* 悬浮表头单元格伪类 */
.th:hover {
  /* 当鼠标悬停时的边框颜色 */
  border-color: black !important;
}

.th:hover .resizeHandler {
  display: block;
}

/* 按钮 */
.Button {
  cursor: pointer;
  position: absolute;
  width: 80px;
  height: 20px;
  top: -20px;
  left: 0;
  /* background-color: aqua; */
}

/* 按钮图像 */
.Button img {
  position: absolute;
  left: 0;
  bottom: 0;
  height: 20px;
  width: 20px;
  /* 不可选中文字 */
  user-select: none;
}

.mutiAttributeSum .Button {
  top: -40px;
}

.mutiAttributeSum .sumAttribute .Button {
  top: -20px;
}

/* 调整大小的手柄 */
.resizeHandler {
  position: absolute;
  top: 0;
  right: -9px;
  bottom: 0;
  width: 9px;
  cursor: ew-resize;
  background-color: black;
  display: none;
  z-index: 3;
}

.sumAttribute:hover .resizeHandler {
  display: block;
}

.Country .movePosition {
  position: absolute;
  top: 0;
  right: 0px;
  bottom: 0;
  width: 6px;
  background-color: red;
  z-index: 2;
  opacity: 0;
  transition: opacity 0.3s;
}

/* 接收移动的位置 */
.movePosition {
  position: absolute;
  top: 0;
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


#sum {
  position: absolute;
  top: -20px;
  width: 100%;
  background-color: #f0f0f0;
  border: 1px solid white;
  transition: border-color 0.3s;
  text-align: center;
}

#sum:hover {
  border-color: red;
}

.mutiAttributeSum {
  /* cursor: pointer; */
  position: relative;
  border: 1px solid white;
  transition: border-color 0.3s;
  height: 100px;
  min-width: 80px;
  top: -20px;
  /* background-color: blueviolet; */
}

#attributeContainer {
  position: relative;
  top: 20px;
  height: 80px;
  display: flex;
  flex-direction: row;
  /* background-color: red; */
}

.sumAttribute {
  position: relative;
  height: 80px;
  /* width: 80px; */
  border: 1px white solid;
}

.weightNum {
  position: relative;
  left: 20px;
}

/************************************** tbody部分 */
.tbody {
  position: relative;
  display: flex;
  flex-direction: column;
}

/* 行 */
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

/* tbody单元格 */
.td {
  position: relative;
  width: 80px;
  height: 20px;
  text-overflow: ellipsis;
  /* 可选，将文本截断并显示... */
  white-space: nowrap;
  /* 防止文本换行 */
  overflow: hidden;
  /* 不可选中文字 */
  user-select: none;
  border: 1px solid white;
}

/* 颜色百分比填充单元格 */
.percentage-cell {
  position: relative;
  width: 80px;
  height: 20px;
  border: 1px solid white;
}

/* before伪元素 */
.percentage-cell::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: var(--fill-percentage);
  background-color: var(--color);
}

/*************************************attributesHub */
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

.attributesHub {
  /* background-color: blue; */
  width: 100%;
  height: 10%;
  position: relative;
  display: flex;
  flex-direction: row;
}

.snapShots {
  position: relative;
  top: 60px;
  display: flex;
  flex-direction: row;
}

.snapShot {
  position: relative;
  display: flex;
  flex-direction: column;
  /* height: 100%; */
  font-size: 5px;
  user-select: none;
}
</style>