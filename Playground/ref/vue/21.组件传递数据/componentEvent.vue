<template>
    <p>组件事件</p>

    <child @someEvent = "getHandle" /><!-- 接受了child的自定义事件！ -->
    <p>{{ msg }}</p><!-- 从child传过来的值，赋值给了这个文件的本地变量 -->
</template>

<script>
    import child from './child21.vue';
    export default{
        data(){
            return{
                msg:""
            }
        },
        component:{
            child
        },
        method:{
            getHandle(data){
                console.log("接到了child的传递数据：",data)
                this.msg = data
            }
        }
    }
</script>