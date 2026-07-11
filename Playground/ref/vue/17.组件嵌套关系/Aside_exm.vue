<template>
    <div class="aside">
        <h3>Aside</h3>
        <Item1 />
        <Item1 />
        <Item1 />   <!-- 是的没错会显示3个同样的item组件 -->
    </div>
</template>

<script>
import { Component } from "react";
import Item1 from "./Item_exm.vue"
export default{
    Component:{
        Item1
    }
}
</script>

<style scoped>
    .aside{
        float: right;
        width:30%;
        height:400px;
        border: 5px solid #999;
        box-sizing: border-box;
    }
</style>