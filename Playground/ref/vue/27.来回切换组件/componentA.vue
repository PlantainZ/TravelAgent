<template>
    <h3>conponentA</h3>
    <p>{{message}}</p>
    <button @click="updateHandle">更新数据</button>
</template>

<script>
    export default {
        data(){
            return{
                message:"老数据"
            }
        },
        beforeUnmount(){
            console.log("组件卸载之前");
        },
        unmounted(){
            console.log("组件卸载之后");
        },
        methods:{
            updateHandle(){
                this.message="新数据";
            }
        }
</script>