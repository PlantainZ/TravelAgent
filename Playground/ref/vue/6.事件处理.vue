> Path : ./myvue/src/components/EventDemo1.vue
> Path : ./myvue/src/components/EventDemo2.vue

# 事件处理

单独对事件做了处理

可以使用 `v-on` 指令(简写为'@')来监听 DOM 事件，并在事件触发时执行对应的JavaScript。

语法：

`v-on:click="methodName"`

`@click="methodName"`

* 内联事件处理器<br>
  事件被触发时，执行内联的JavaScript语句，与 onclick 类似
* 方案事件处理器
  一个指向组件上定义的方法的属性名或是路径

# 内联事件处理器

```vue

<template>
    <div>内联事件处理器的代码编写</div>
    <button @click="count++">Add</button>
    <p>{{ count }}</p>
</template>

<script>
    export default {
        data() {
            return {
                count: 1
            }
        }
    }
</script>
```

# 方法事件处理器

> methods: {<br>
> 方法1 () { 方法体1 }<br>
> 方法2 () { 方法体2 }<br>
> }

```vue

<template>
    <div>方法事件处理器</div>
    <button @click="addCountFunc">add</button>
    <p>Count is : {{ count }}</p>
</template>
<script>
    export default {
        data() {
            return {
                count: 1
            }
        },
        // 所有的方法都写在 methods 之中
        methods: {
            addCountFunc() {
                console.log('addCountFunc');
                this.count++;
            }
        }
    }
</script>
```