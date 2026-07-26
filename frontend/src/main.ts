import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'


import Antd from 'ant-design-vue' // 1. 把整个 Ant Design 组件库搬进来
import 'ant-design-vue/dist/reset.css' // 2. 把 Ant Design 的样式搬进来

import App from './App.vue'
import Home from './views/Home.vue'
import Result from './views/Result.vue'
import TestRouter from './views/testRouter.vue'
import TestRouterComponent from './views/testRouterComponent.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'homePage',
      component: Home
    },
    // {
    //   path: '/result',
    //   name: 'Result',
    //   component: Result
    // },
    {
      path: '/testRouter',
      name: 'testRouter',
      component: TestRouter,
      children:[
        {
          path:'/Result',
          name:'Result',
          component:()=>import('./views/Result.vue')
        },
        {
          path:'/ItineraryOv',
          name:'ItineraryOv',
          component:()=>import('./views/ItineraryOv.vue')
        },
        {
          path:'/TicketRsvt',
          name:'TicketRsvt',
          component:()=>import('./views/TicketRsvt.vue')
        },
      ]
    },
    {
      path: '/testRouterComponent',
      name: 'testRouterComponent',
      component: TestRouterComponent
    },
  ],

  scrollBehavior(){
    return{ top:0 } // 切换页面时滚动到顶部
  }
})

const app = createApp(App)

app.use(router) // wow终于认识你了

app.use(Antd) // 3. 全局注册。告诉 Vue：“所有 Ant 组件，以后随便用”

app.mount('#app')

