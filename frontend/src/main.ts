import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'


import Antd from 'ant-design-vue' // 1. 把整个 Ant Design 组件库搬进来
import 'ant-design-vue/dist/reset.css' // 2. 把 Ant Design 的样式搬进来

import App from './App.vue'
import Home from './views/Home.vue'
import Result from './views/Result.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'backFile',
      component: Home
    },
    {
      path: '/result',
      name: 'Result',
      component: Result
    }
  ]
})

const app = createApp(App)

app.use(router)

app.use(Antd) // // 3. 全局注册。告诉 Vue：“所有 Ant 组件，以后随便用”

app.mount('#app')

