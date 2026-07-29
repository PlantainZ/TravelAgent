<template>
  <a-layout style="min-height: 100vh">
    
    <!-- ====== 侧边导航区域：永远存在，不参与过渡动画 ====== -->
    <a-layout-sider
      v-model:collapsed="collapsed"
      :trigger="null"
      collapsible
      width="240"
      style="
        background: #fff;
        border-right: 1px solid #f0f0f0;
        position: relative;
        z-index: 10;
      "
    >
      <div class="logo">
        <h2>档案详情</h2>
      </div>          <!--这个可以不要-->

      <!-- 你原来的 a-affix 固定导航 -->
      <!-- <div class="side-nav">
        <a-affix :offset-top="80">
          <a-menu
            v-model:selectedKeys="selectedKeys"
            mode="inline"
            @click="handleMenuClick"
          >
            <a-menu-item key="/">
              <template #icon><HomeOutlined /></template>
              <span>首页</span>
            </a-menu-item>
            <a-menu-item key="/testRouterComponent">
              <template #icon><AppstoreOutlined /></template>
              <span>testRouterComponent</span>
            </a-menu-item>
            <a-menu-item key="/about">
              <template #icon><InfoCircleOutlined /></template>
              <span>关于</span>
            </a-menu-item>
            <a-menu-item key="/contact">
              <template #icon><MailOutlined /></template>
              <span>联系我们</span>
            </a-menu-item>
          </a-menu>
        </a-affix>
      </div> -->

      <div v-if="tripPlan" class="side-nav">
        <a-affix :offset-top="80">
          <a-menu mode="inline" :selected-keys="[activeSection]" @click="handleMenuClick">
            <!-- scrollToSection本来是点击侧边栏滚动到指定区域-->

            <a-menu-item key="/Result"><!-- 挂载切换 查看前后端链接ItineraryOv -->
              <span>📋 档案总览</span>
            </a-menu-item>

            <a-sub-menu key="preWork" title="☄️前置准备">
              <a-menu-item key="/TicketRsvt">
                票务 / 预约
              </a-menu-item>
              <a-menu-item key="/ItemList">
                <span>准备物品清单</span>
              </a-menu-item>
              <a-menu-item key="localInfoSearch" >
                当地信息查询：暂未开放
              </a-menu-item>
            </a-sub-menu>


            <a-sub-menu key="days" title="📅 我的行程">
              <a-menu-item key="/trvlEdit"> <!-- 测试testRouter噢 -->
                <span>行程编辑</span>
              </a-menu-item>
              <a-menu-item v-for="(day, index) in tripPlan.days" :key="`day-${index}`">
                第{{ day.day_index + 1 }}天
              </a-menu-item>
            </a-sub-menu>

            <a-menu-item key="specialEvent">
              <span>📋 特别活动</span>
            </a-menu-item>

            <a-menu-item key="teamQA">
              <span>🔱组内Q&A</span>
            </a-menu-item>

            <a-menu-item key="elseCheck">
              <span>🚨其它调查</span>
            </a-menu-item>

            <!-- <a-menu-item key="budget" v-if="tripPlan.budget"> -->
              <!-- <span>💰 预算明细</span> -->
            <!-- </a-menu-item> -->

            <a-menu-item key="map">
              <span>景点地图</span>
            </a-menu-item>

            <!-- <a-menu-item key="weather" v-if="tripPlan.weather_info && tripPlan.weather_info.length > 0"> -->
              <!-- <span>🌤️ 天气信息</span> 还要综合到行程概览里去！！！ -->
            <!-- </a-menu-item> -->

            <a-menu-item key="archiveConfig">
              <span>🍁档案设置</span>
            </a-menu-item>

          </a-menu>
        </a-affix>
      </div>


    </a-layout-sider>

    <!-- ====== 右侧内容区域：参与渐隐渐显过渡 ====== -->
    <a-layout-content
      style="
        padding: 24px;
        background: #f5f5f5;
        overflow-y: auto;
        position: relative;
      "
    >
      <!-- 
        关键：用 Vue 的 <Transition> 包裹 <router-view>
        mode="out-in" 表示：先渐隐旧页面，再渐显新页面
      -->
      <router-view v-slot="{ Component, route }">
        <Transition name="fade-transform" mode="out-in">
          <!-- 
            :key="route.path" 确保不同路由的组件被视为不同元素，
            从而触发过渡动画（即使两个路由使用了相同组件）
          -->
          <component :is="Component" :key="route.path" />
        </Transition>
      </router-view>
    </a-layout-content>
  </a-layout>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  HomeOutlined,
  AppstoreOutlined,
  InfoCircleOutlined,
  MailOutlined,
} from '@ant-design/icons-vue'


import type { TripPlan } from '@/types'

const route = useRoute()
const router = useRouter()
const collapsed = ref(false)
const tripPlan = ref<TripPlan | null>(null)

onMounted(async () => {
  const data = sessionStorage.getItem('tripPlan')
  if (data) {
    tripPlan.value = JSON.parse(data)
    console.log("这是tripPlan的value:",tripPlan.value)
    // 加载景点图片
    // await loadAttractionPhotos()
    // 等待DOM渲染完成后初始化地图
    // await nextTick()
    // initMap()
  }
})


// 迁移来的nav 所需组件================================
const activeSection = ref('overview')
// 点击菜单项 → 跳转
const handleMenuClick = ({ key }) => {
  router.push(key)
}

// 根据当前路由路径同步菜单选中状态
const selectedKeys = ref([route.path])

watch(
  () => route.path,
  (newPath) => {
    selectedKeys.value = [newPath]
  }
)

</script>

<style scoped>
.logo {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #f0f0f0;
}

.logo h2 {
  margin: 0;
  font-size: 18px;
  color: #1890ff;
}

/* .side-nav {
  padding: 8px 0;
} */

.side-nav {
  width: 240px;
  flex-shrink: 0;
}

/* ============================================
   渐隐渐显 + 轻微位移 过渡动画（核心 CSS）
   ============================================ */

/* 进入和离开的过渡持续时间 */
.fade-transform-enter-active,
.fade-transform-leave-active {
  transition: opacity 0.35s ease, transform 0.35s ease;
}

/* 进入过渡的起始状态：透明 + 向右偏移 20px */
.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

/* 进入过渡的结束状态：完全不透明 + 无偏移 */
.fade-transform-enter-to {
  opacity: 1;
  transform: translateX(0);
}

/* 离开过渡的起始状态：完全不透明 + 无偏移 */
.fade-transform-leave-from {
  opacity: 1;
  transform: translateX(0);
}

/* 离开过渡的结束状态：透明 + 向左偏移 20px */
.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>