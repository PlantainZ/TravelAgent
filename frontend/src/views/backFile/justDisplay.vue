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
        <h2>My App</h2>
      </div>

      <!-- 你原来的 a-affix 固定导航 -->
      <div class="side-nav">
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
            <a-menu-item key="/products">
              <template #icon><AppstoreOutlined /></template>
              <span>产品</span>
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

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  HomeOutlined,
  AppstoreOutlined,
  InfoCircleOutlined,
  MailOutlined,
} from '@ant-design/icons-vue'

const route = useRoute()
const router = useRouter()
const collapsed = ref(false)

// 根据当前路由路径同步菜单选中状态
const selectedKeys = ref([route.path])

watch(
  () => route.path,
  (newPath) => {
    selectedKeys.value = [newPath]
  }
)

// 点击菜单项时进行路由跳转
const handleMenuClick = ({ key }) => {
  router.push(key)
}
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

.side-nav {
  padding: 8px 0;
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