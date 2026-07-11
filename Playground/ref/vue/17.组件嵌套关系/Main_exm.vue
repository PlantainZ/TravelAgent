<template>
    <div class="main">
        <h3>Main</h3>
        <Article1 />
        <Article1 /> <!-- 是的没错会显示两遍哦 -->
    </div>
</template>

<script>
import { Component } from "react";
import Article1 from "./Article_exm.vue"
export default {
    Component:{
        Article1
    }
}
</script>

<style scoped>
.main{
    float: left;
    width:70%;
    height:400px;
    border: 5px solid#999;
    box-sizing:border-box;
    border-top:0px;
}
</style>