<template>
    <h3>Slots再续集</h3>

    <slot :msg="childMessage"> </slot> <!-- 通过:props的形式传递给了父元素！ -->
    <slot name = "header" :job="se"> </slot> 
</template>

<script>
    export default {
        data(){
            return{
                childMessage:"子组件数据",
                se:"具名插槽传递"
            }
        }
    }
</script>