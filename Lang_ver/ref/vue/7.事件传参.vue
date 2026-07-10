> Path : ./myvue/src/components/EventDemo3.vue
> Path : ./myvue/src/components/EventDemo4.vue

```vue

<template>
    <div>
        <p>{{ count }}</p>
        <button @click="addFunc('addFunc()')" :style="fontSize"> +</button>
    </div>
    <br>
    <div>
        <p>事件传参</p><!-- 是通过click里的函数括号，传到函数里执行了，后台会打印传入的信息！ -->
                      <!-- 要小心，$event务必要作为最后一个参数传入 -->
        <p v-for="(item,index) of nums" @click="useButton(item,$event)" :key="index">{{ item }}</p>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                count: 0,
                fontSize: "font-size:30px;",
                nums: ["aom", "som", "dom"],
            }
        },
        methods: {
            addFunc(e) {
                // Vue中的event
                console.log(e) // e就是btn元素对象本身
                e.target.innerHTML = "+,当前count值："+this.count // 按钮名称会改变哦！
                this.count++;
            },
            useButton(inSting, e) {
                console.log(inSting);
                console.log(e);
            }
        }
    }
</script>
```