<template>
    <h3>Parent</h3>
    <Child title="来自Parent的数据"
            :checkType = "checkType"/> <!-- 从这里传数据去child -->
</template>

<!-- 注意！！！只能从父级传递到子级。逆行全责！！！-->

<script>
    import Child from "./Child.vue"
    export default {
        data(){
            return{
                checkType:"标题"
            }
        },
        components:{
            Child
        }
</script>