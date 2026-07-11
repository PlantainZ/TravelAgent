import { createApp } from 'vue'
import App from './App.vue'

// app是根组件，main.js引入了app.vue，从app.vue再层层嵌套其它组件
const app = createApp(App) // 在一个vue项目中，有且只有一个vue示例对象

// 在所有vue文件里，都可以获取这个变量！
app.provide("golabData","我是全局数据")

app.mount('#app') // 除了实例化，还需要手动挂载！
// 这里的#app，要找index.html！！！里面有一个id为app的div!
// 以后vue的所有内容都要放进这个叫app的div中呈现
// 所有vue文件最后都会被编译成一个main.js，在这个div内实现。

/*
    浏览器可执行文件：HTML & SCRIPT & CSS，以及图片Image
    构建工具：Webpack、vite（浏览器的编译工具）
*/