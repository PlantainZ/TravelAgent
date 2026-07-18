<template>
  <!-- handleClick 就是点击事件触发时的回调函数 -->

什么是回调函数？ 生活中的比喻：点外卖

假设你去餐厅点了一份需要现做的披萨：
    同步执行 (不用回调)：你站在柜台死等，直到披萨烤好你才离开。这期间你什么也干不了（程序阻塞）。
    异步执行 (使用回调)：你点完餐后，给前台留一个手机号码，然后去逛街。
                        披萨烤好后，前台拨打你留下的号码通知你取餐。

在这里，“你留下的手机号码及接电话后的动作”，就是回调函数 (Callback Function)。

回调函数不是一个新的语法，而是一种编程模式：
    把函数 A 作为参数，传递给另一个函数 B，
    由函数 B 决定在合适的时候（比如异步操作完成、事件触发时）去调用函数 A。

  <button @click="handleClick">点赞</button>
</template>

<script setup>
import { ref } from 'vue';
const likes = ref(0);

// 事件回调函数
// 浏览器在监听到 click 事件时，会自动调用这个函数，并传入事件对象 (event)
const handleClick = (event) => { // 是的，这是一个函数。在js里，函数和变量是平等的。
                                // const确保这个名称不会指向别的功能，或者变量。
  likes.value++;
  console.log('按钮被点击了，当前坐标：', event.clientX, event.clientY);
};
</script>