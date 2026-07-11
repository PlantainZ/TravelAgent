<template>
    <h3>Parent</h3>
    <Child />
    <p>我是parent里显示的全局数据哦：{{ globalData  }}</p>
</template>

<script>
    import Child from "./Child.vue"
    export default {
        inject:['globalData'],
        components:{
            Child
        }
    }
</script>