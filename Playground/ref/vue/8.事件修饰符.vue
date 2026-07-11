> import ArrayList from "./components/ArrayList.vue";
```vue
<template>
    <h3>事件修饰符</h3>
    <!-- 【1】阻止默认事件 -->
    <a href="https://bing.com" @click="clickHandle1($event)">百度</a>

    <!-- 【2】阻止父级标签的事件 -->
    <div @click="clickDiv">
        <p @click="clickP1">
            测试
            <!--clickP-子事件,clickDiv-父事件-->
        </p>
    </div>
    <div @click="clickDiv">
        <p @click="clickP2">
            测试
            <!--clickP-子事件-->
        </p>
    </div>
    <div @click="clickDiv">
        <p @click.stop="clickP1"> <!--这样的话，就会阻止事件传播，原本会传到div的click事件就不会触发了-->
            测试
            <!--clickP-子事件-->
        </p>
    </div>
</template>

<script>
export default {
    data() {
        return {}
    },
    methods: {
        clickHandle1(e) {
            // e.preventDefault：阻止默认事件
            e.preventDefault()
            console.log('clickHandle1');
        },
        clickHandle2() {
            console.log('clickHandle2');
        },
        clickDiv(){
            console.log('clickDiv-父事件');
        },
        clickP1(e){
            console.log('clickP-子事件');
        },
        clickP2(e){
            e.stopPropagation(); // 尽量不要在函数里面处理DOM事件，关注逻辑本身。用stop！！！
            console.log('clickP-子事件');
        }
    }
}
</script>
```