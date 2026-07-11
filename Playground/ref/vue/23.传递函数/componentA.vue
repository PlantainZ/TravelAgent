<template>
    <h3>ComponentA</h3>
    <ComponentB :onEvent = "dataFn"/> <!-- 这是父传子！ -->
    <p>父元素：{{ msg }}</p>
</template>

<script>
    import ComponentB from "./ComponentB.vue"
    export default {
        data(){
            return{
                msg:""
            }
        },
        components:{
            ComponentB
        },
        method: {
            dataFn(data){
                this.msg = data
            } // 传给componentB了哦！
        }
    }
</script>