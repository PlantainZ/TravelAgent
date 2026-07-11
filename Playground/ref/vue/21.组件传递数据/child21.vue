<template>
    <h3>Child</h3>
    <button @click="clickEventHandle"> 子传父传递试验 </button>

</template>

<script>
    export default {
        method:{
            clickEventHandle(){
                this.$emit("someEvnet","child数据") // 字符串内是事件类型
            }
        }
    }

</script>