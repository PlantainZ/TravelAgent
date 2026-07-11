> import ClassDemo from "./components/ClassDemo.vue";

```vue
<template>
    <!-- 可以接收一个对象 isActive -->
    <p :class="{'active':isActive,'text-danger':hasError}">
        Class样式绑定1
    </p>

    <p :class="classObject">Class样式绑定2</p> <!-- 通过集合一劳永逸 -->

    <p :class="[arrActive,arrHasError]">Class样式绑定3</p>

    <p :class="[isActive? 'active': '' ]">Class样式绑定4</p>

    <div :class="[{'active':isActive },errorclass]">class样式绑定5</div>

    <!-- 数组里面是可以有对象的哦！不冲突 -->
    <p :class="[isActive? 'active': '' ,{'text-danger':hasError} ]">Class样式绑定4</p>
</template>

<script>
export default {
    data() {
        return {
            isActive: true,  // 如果是false的话，下面的active样式就不显示了
            hasError: false, // 如果是true的话，字体会变成红色哦

            classObject: { // 2.可以通过一个集合一劳永逸！
               'active': true,
               'text-danger': true
             },

            // 3.当然也可以是数组关系....↓
            arrActive:"active",
            arrHasError:"text-danger",

            // 5.当数组和对象一起出现时。。。。
            errorclass:"text-danger"
        }
    },
    methods: {},
    computed: {}
}
</script>


<style>

  .active {
    font-size: 30px;
  }

  .text-danger {
    color: red;
  }

</style>
