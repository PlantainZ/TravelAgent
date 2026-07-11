<template>
    <h3>child</h3>
    <p>{{ message }}</p>
    <p>{{ fullMsg }}</p>
    <p>{{ globalData }}</p>
</template>

<script>
export default{
    inject:['message','globalData'], // 不经过parent直接拿到爷爷的财产！这就是依赖注入
    data(){
        return{
            fullMsg:this.message // 将依赖注入里获得的数据赋值给本地变量
        }
    }
}
</script>