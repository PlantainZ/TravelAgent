<template>
    搜索：<input type="text" v-model="search">
</template>

<script>
    export default {
        data(){
            return{
            search:""
            }
        },

        //侦听器：一旦v-model的search发生变化
        //      就会通过监听器emit一个叫searchEvent的事件，
        //      附带一个newValue
        watch:{
            search(newValue,oldValue){
            this.$emit("searchEvent",newValue)
            }
        }
</script>