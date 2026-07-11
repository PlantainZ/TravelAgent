<template>
    <h3>ComponentB</h3>
    <p>{{ title }}</p>

    <p>{{onEvent("传递数据")}}</p> <!-- 调用的是A里的dataFn哦！-->
</template>

<script>
    export default {
        data(){
            return{}
        },
        props:{
            title:String,
            onEvent:Function // 传递过来的是函数！
        }
</script>