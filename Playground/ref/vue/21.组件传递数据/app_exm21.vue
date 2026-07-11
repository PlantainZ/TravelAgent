<!-- props & $emit 的区别

 - props 数据只能父传子
 - $emit 自定义事件可以子传父！！！

-->

<!-- 这里只是为了观察componentEvent.vue，移步另外两个vue观察 -->
<template>
    <ComponentEvent />
</template>

<script>
    import ComponentEvent from"./ComponentEvent.vue"
    export default {
        components:{
            ComponentEvent
        }
    }
</script>