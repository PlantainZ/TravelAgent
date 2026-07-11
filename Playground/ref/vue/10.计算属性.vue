> import ComputerDemo from "@/components/ComputerDemo.vue";

methods和computed的区别？

【1】methods方法调用总是会在重新渲染的时候再次执行函数
    人话：多次展示同一个变量，这个变量值，每展示一次，就要计算一次。很多重复无意义的工作。

【2】computed计算属性会基于响应式依赖被缓存，一个计算属性仅会在其响应式依赖更新时才重新计算
    人话：多次展示同一个变量，这个变量值是一次计算的结果。

<script>
    export default {
        data() {
            return {
                some: {
                    names: "SuperPinnacle",
                    content: ["Python", "java", "C"]
                }
            }
        },

        methods: {
            // 函数定义
        },
        /*
        * computed : { 计算属性 }
        * 将模板语法里面的复杂表达式存放到计算属性之中
        * */
        computed: {
            someContent() {
                return this.some.names.length > 0 ? "Yes" : "No"
            }
        }
    }
</script>

<template>
    <h3>{{ some.names }}</h3>
    <p>{{ someContent }}</p>  <!-- 这是computed函数，直接展示结果 -->

</template>
```