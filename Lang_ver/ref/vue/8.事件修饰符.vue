> import ArrayList from "./components/ArrayList.vue";
```vue
<template>
    <h3>事件修饰符</h3>
    <!-- 【1】阻止默认事件 -->
    <a href="https://bing.com" @click="clickHandle1($event)">百度</a>
    <a href="https://bing.com" @click.prevent="clickHandle2">百度</a>
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
        <p @click.stop="clickP1">
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
            e.stopPropagation();
            console.log('clickP-子事件');
        }
    }
}
</script>
```