<template>
  <RouterView/>
</template>

<script>
import { RouterView } from 'vue-router'
import { useCounterStore } from './stores/counter'

export default {
  name: 'App',
  data() {
    return {
      store: useCounterStore(),
    }
  },

  created() {
    if (this.store.loaded) return;
    this.store.getData();
  },
}
</script>

<style>
</style>