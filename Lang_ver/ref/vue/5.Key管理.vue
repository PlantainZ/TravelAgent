
<template>
    <div>
        <!-- key这里是通过v-bind绑定的特殊attribute，减少渲染消耗 -->
        <!-- 建议在任何时候都为v-for添加一个key，kye绑定的期望数值，是一个基础型的数值，例如字符串或者number类型 -->
        <!-- 一般就是字典元素里，item自带的一长串防伪id ，不推荐用index作id-->
        <p v-for="(s,index) in some" :key="index"> <!-- 注意冒号 -->
            {{ s }}的下标是:{{ index }}
        </p>
        <!-- 在实际生产环境中，推荐使用每一条数据的id作为key -->
    </div>
</template>
<script>
    export default {
        data() {
            return {
                some: ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
            }
        }
    }
</script>