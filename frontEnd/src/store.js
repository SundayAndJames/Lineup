import { reactive } from 'vue';

const state = reactive({
  count: 0
});

const methods = {
  increment() {
    state.count++;
  }
};

export default {
  state,
  methods
};
