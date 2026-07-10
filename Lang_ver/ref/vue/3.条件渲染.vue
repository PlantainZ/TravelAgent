> Path : ./myvue/src/components/IfDemo.vue

# v-if和v-show的区别？

## （1）v-if

v-if是真实的按照条件进行的渲染，因为它确保了在切换时，条件块内的时间监听器和子组件都会被销毁或者重建

v-if是惰性的，因为如果在初始渲染时条件值为false，则不会做任何事情，条件区块只有当条件首次变为true时才会被渲染

## （2）v-show

相对比之下，v-show简单许多，无论初始条件如何，始终会被渲染，显示和不显示只有css的display属性会被切换

## （3）总结

总的来说，v-if的功能模型更多，但是具有更高的功能开销，而v-show具有更高的初始渲染开销

因为如果需要频繁切换，则使用v-show比较好，如果在运行时绑定条件很少改变，则v-if会更加契合

# Codes

```vue
<template>
    <h3>条件渲染</h3>

    <!-- v-if 和 v-else 属于同一个模块，两者只能生效其一 -->
    <div v-if="flag">你可以看见我吗?</div>
    <div v-else>不能看见我</div>

    <!-- v-else-if 多个块使用 -->
    <div v-if="type==='A'">A</div>
    <div v-else-if="type==='B'">B</div>
    <div v-else-if="type==='C'">C</div>

    <!-- v-show -->
    <div v-show="flag">你可以看见我</div>
</template>

<script>
export default {
    data() {
        return {
            // flag 为 true ，可以显示，反之无法显示
            flag: true,
            type: "B"
        }
    }
}
</script>
```