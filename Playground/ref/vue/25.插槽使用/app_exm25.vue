<template>
    <SlotsBase> <!-- 不再是单标签<SlotsBase /> 了哦！！！ -->
        <div>
            <h3>插槽标题</h3>
            <p>插槽内容</p>
        </div>
    </SlotsBase>

    <SlotsTwo>
        <h3>{{ msg }}</h3><!-- 虽然是写在父元素，但却是在子组件中渲染的-->
    </SlotsTwo>

</template>

<script>
    import SlotsBase from "./components/SlotsBase.vue"
import SlotsTwo from "./slotsTwo.vue";
    import slotsTwo from "./slotsTwo.vue";
    export default {
        data(){
            return{
                msg:"插槽内容Two"
            }
        },
        components:{
            SlotsBase
        }
    }
</script>

<style>
</style>