> import WatchDemo from "@/components/WatchDemo.vue";

# 关键字：watch{}

```vue
<!--
    数据监听器，可以监听return中的数据
-->
<template>
    <h3>监听器</h3>
    <p>{{ message }}</p>
    <button @click="updateHandle">修改数据</button>
</template>

<script>
export default {
    data() {
        return {
            message: 1
        }
    },
    methods: {
        updateHandle() {
            this.message = this.message + 1
        }
    },
    watch: {
        // 函数名必须与侦听的数据对象保持一致
        // 监听变量(newVal新值,oldVal旧值){函数体}
        message(newVal, oldVal) {
            // 数据发生变化时，自动执行的函数
            console.log("newVal : ", newVal, " ; ", "oldVal : ", oldVal)
        }
    }
}
</script>
```