<template>
    <h3>插槽父子变量一起使用示例</h3>

    <SlotTogether v-slot="slotProps"> <!-- 通过v-slot的形式接收了子元素的数据，
                                        slotProps是对象类型，里面接收了传过来的数据 -->
            <h3>{{ currentTest }}-{{ slotProps.msg }}</h3> <!-- msg是子元素的变量名哦 -->
    </SlotTogether>

    <SlotTogether>
        <template #header="slotProps">
            <h3>{{ slotProps.job }}</h3>
        </template>
    </SlotTogether>
</template>

<script>
import SlotTogether from './slotTogether.vue';
import SlotTogether from './slotTogether.vue';
export default{
    data(){
        return{
            currentTest:"测试内容" //这是属于父元素自己的变量哦
        }
    },
    component:{
        SlotTogether
    }
}

</script>