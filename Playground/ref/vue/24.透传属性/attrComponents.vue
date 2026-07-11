<template>
    <!-- 必须是唯一的根元素！！！比如如果存在h4，它就不生效了 -->
    <h3>透传属性</h3>
</template>

<script>
export default{
    inheritAttrs:false // 可以阻止透传属性！
}
</script>

<style>
    .attr-container{
        color: red;
    }
    
</style>