<template>
  <div class="jumbotron">
    <!-- 标题区域：对应原 b-jumbotron 的 header 属性 -->
    <h1 v-if="header" class="jumbotron-header">{{ header }}</h1>
    
    <!-- 引导语区域：对应原 b-jumbotron 的 lead 属性 -->
    <p v-if="lead" class="jumbotron-lead">{{ lead }}</p>
    
    <!-- 默认插槽：用于放置内部的 <p> 和 <button> 等内容 -->
    <slot></slot>
  </div>
</template>

<script setup>
// 定义 Props，保持与原组件相似的数据传递方式
defineProps({
  header: {
    type: String,
    default: ''
  },
  lead: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
/* ==========================================
   1. Jumbotron 容器样式 (复刻 Bootstrap 4)
   ========================================== */
.jumbotron {
  padding: 2rem 1rem;
  margin-bottom: 2rem;
  background-color: #e9ecef; /* Bootstrap 经典的浅灰背景 */
  border-radius: 0.3rem;
  color: #212529; /* 默认文本颜色 */
}

/* 响应式适配：在大于 576px 的屏幕上增加内边距 */
@media (min-width: 576px) {
  .jumbotron {
    padding: 4rem 2rem;
  }
}

/* ==========================================
   2. 标题样式 (复刻 h1 / display 效果)
   ========================================== */
.jumbotron-header {
  font-size: 2.5rem;
  font-weight: 300; /* 轻字重，巨幕组件的核心特征 */
  line-height: 1.2;
  margin-top: 0;
  margin-bottom: 0.5rem;
}

@media (min-width: 576px) {
  .jumbotron-header {
    font-size: 3.5rem; /* 大屏幕下放大标题 */
  }
}

/* ==========================================
   3. 引导语样式 (复刻 .lead 类)
   ========================================== */
.jumbotron-lead {
  font-size: 1.25rem;
  font-weight: 300;
  line-height: 1.5;
  margin-bottom: 1rem;
}

/* ==========================================
   4. 按钮样式 (复刻 .btn .btn-primary)
   ========================================== */
/* 使用 :deep() 确保插槽内的按钮也能应用样式 */
:deep(.btn-primary) {
  display: inline-block;
  font-weight: 400;
  text-align: center;
  white-space: nowrap;
  vertical-align: middle;
  user-select: none;
  text-decoration: none;
  
  /* 核心颜色与尺寸 */
  color: #fff;
  background-color: #007bff;
  border: 1px solid #007bff;
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  line-height: 1.5;
  border-radius: 0.25rem;
  cursor: pointer;
  
  /* 平滑过渡动画 */
  transition: color 0.15s ease-in-out, 
              background-color 0.15s ease-in-out, 
              border-color 0.15s ease-in-out;
}

/* 按钮 Hover 状态 (颜色加深) */
:deep(.btn-primary:hover) {
  color: #fff;
  background-color: #0069d9;
  border-color: #0062cc;
}

/* 按钮 Focus/Active 状态 */
:deep(.btn-primary:focus),
:deep(.btn-primary:active) {
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}
</style>