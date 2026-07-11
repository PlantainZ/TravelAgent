<template>
    <Header />  <!-- 这里是全局注册过了！ -->
    <Main />
    <Aside />
</template>

<script>
    // import Header from "./Header_exm.vue"
    import Main from "./Main_exm.vue"
    import Aside from "./Aside_exm.vue"
    export default {
        components:{
            // Header,
            Main,
            Aside
        }
    }
</script>

<style>
</style>

<!--
一般默认的层级关系：

        <Header>
<Root>  <Main>    <Article> x2
        <Aside>   <Item> x3

-->