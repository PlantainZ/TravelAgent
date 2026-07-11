
<template>
  <h3>数组变化侦听</h3>
  <button @click="addListHandle">添加数据</button>
  <ul>
    <li v-for="(item,index) of names" :key="index">{{ item }}</li>
  </ul>
</template>

<script>
  export default {
    data() {
      return {
        names: ["iwen", "ime", "frank"]
      }
    },
  methods: {
    addListHandle() {
      // 引起UI自动更新
      // this.names.push("sakura")

      // 如果没有赋值给this.names，不会引起UI自动更新
      this.names = this.names.concat(["sakura"])
    }
  }
}
</script>