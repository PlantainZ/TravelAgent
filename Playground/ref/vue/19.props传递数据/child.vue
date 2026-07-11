<template>
    <h3>Chile</h3>
    <p>{{ title }}</p>
    <p>{{ msg }}</p>

    <ul>
        <!-- 还可以传递数组类型哦 -->
        <li v-for="(item,index) in names" :key="index"></li>
    </ul>
    <p>{{ useInfo.name }}</p>
    <p>{{ useInfo.age }}</p>


</template>

<script>
import { useReducer } from 'react';

    export default {
        data(){
            return{}
        },
        props:["title","msg","name","userInfo"] // 数据来自parent，要用字符串方式存在！！
    }

</script>