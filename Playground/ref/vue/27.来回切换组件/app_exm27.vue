<template>
    <h3>组件切换</h3>

    <keep-alive><!-- 保持组件及其现有数据依然存活 -->
    <component :is="currentTab"></component> <!-- 这个component :is，就是来回切换的核心！ -->
    </keep-alive>

    <button @click="changeComponentHandle">切换</button>
</template>

<script>
    import ComponentA from ".ComponentA.vue"
    
    //=========这是异步加载哦！==========================
    // import ComponentB from".ComponentB.vue"
    import {defineAsyncComponent } from 'vue'
    constAsyncComponentB = defineAsyncComponen( () =>
            import('./components/ComponentB.vue')
    )
    //================================================== 

    export default{
        components:{
            ComponentA,
            ComponentB
        },
        data(){
            return{
                currentTab:"ComponentA",
            }
        },      
        methods:{
            changeComponentHandle(){
                this.currentTab = this.currentTab =="ComponentA" ?"ComponentB":"ComponentA"
        }
    }
    }
</script>