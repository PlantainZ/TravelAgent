<template>
  <div id = 'conponent'>
    <p> trvlEdit 施工中....正在逐渐显示行程内容......</p>



    <!-- 行程内容 -->
            <a-card title="📅 每日行程" :bordered="false" class="days-card">
          <a-collapse v-model:activeKey="activeDays" accordion>
            <a-collapse-panel v-for="(day, index) in tripPlan.days" :key="index" :id="`day-${index}`">
              <template #header>
                <div class="day-header">
                  <span class="day-title">第{{ day.day_index + 1 }}天</span>
                  <span class="day-date">{{ day.date }}</span>
                </div>
              </template>

              <!-- 行程基本信息 -->
              <div class="day-info">
                <div class="info-row">
                  <span class="label">📝 行程描述:</span>
                  <span class="value">{{ day.description }}</span>
                </div>
                <div class="info-row">
                  <span class="label">🚗 交通方式:</span>
                  <span class="value">{{ day.transportation }}</span>
                </div>
                <div class="info-row">
                  <span class="label">🏨 住宿:</span>
                  <span class="value">{{ day.accommodation }}</span>
                </div>
              </div>

              <!-- 景点安排 -->
              <a-divider orientation="left">🎯 景点安排</a-divider>
              <a-list :data-source="day.attractions" :grid="{ gutter: 16, column: 2 }">
                <template #renderItem="{ item, index }">
                  <a-list-item>
                    <a-card :title="item.name" size="small" class="attraction-card">
                      <!-- 编辑模式下的操作按钮 -->
<!--                      <template #extra v-if="editMode">-->
<!--                        <a-space>-->
<!--                          <a-button size="small" @click="moveAttraction(day.day_index, index, 'up')"-->
<!--                            :disabled="index === 0">-->
<!--                            ↑-->
<!--                          </a-button>-->
<!--                          <a-button size="small" @click="moveAttraction(day.day_index, index, 'down')"-->
<!--                            :disabled="index === day.attractions.length - 1">-->
<!--                            ↓-->
<!--                          </a-button>-->
<!--                          <a-button size="small" danger @click="deleteAttraction(day.day_index, index)">-->
<!--                            🗑️-->
<!--                          </a-button>-->
<!--                        </a-space>-->
<!--                      </template>-->

                      <!-- 景点图片 -->
                      <div class="attraction-image-wrapper">
                        <img :src="getAttractionImage(item.name, index)" :alt="item.name" class="attraction-image"
                          @error="handleImageError" />
                        <div class="attraction-badge">
                          <span class="badge-number">{{ index + 1 }}</span>
                        </div>
                        <div v-if="item.ticket_price" class="price-tag">
                          ¥{{ item.ticket_price }}
                        </div>
                      </div>

                      <!-- 编辑模式下可编辑的字段 -->
<!--                      <div v-if="editMode">-->
<!--                        <p><strong>地址:</strong></p>-->
<!--                        <a-input v-model:value="item.address" size="small" style="margin-bottom: 8px" />-->

<!--                        <p><strong>游览时长(分钟):</strong></p>-->
<!--                        <a-input-number v-model:value="item.visit_duration" :min="10" :max="480" size="small"-->
<!--                          style="width: 100%; margin-bottom: 8px" />-->

<!--                        <p><strong>描述:</strong></p>-->
<!--                        <a-textarea v-model:value="item.description" :rows="2" size="small"-->
<!--                          style="margin-bottom: 8px" />-->
<!--                      </div>-->

                      <!-- 查看模式 -->
                      <div>
                        <p><strong>地址:</strong> {{ item.address }}</p>
                        <p><strong>游览时长:</strong> {{ item.visit_duration }}分钟</p>
                        <p><strong>描述:</strong> {{ item.description }}</p>
                        <p v-if="item.rating"><strong>评分:</strong> {{ item.rating }}⭐</p>
                      </div>
                    </a-card>
                  </a-list-item>
                </template>
              </a-list>

              <!-- 酒店推荐 -->
              <a-divider v-if="day.hotel" orientation="left">🏨 住宿推荐</a-divider>
              <a-card v-if="day.hotel" size="small" class="hotel-card">
                <template #title>
                  <span class="hotel-title">{{ day.hotel.name }}</span>
                </template>
                <a-descriptions :column="2" size="small">
                  <a-descriptions-item label="地址">{{ day.hotel.address }}</a-descriptions-item>
                  <a-descriptions-item label="类型">{{ day.hotel.type }}</a-descriptions-item>
                  <a-descriptions-item label="价格范围">{{ day.hotel.price_range }}</a-descriptions-item>
                  <a-descriptions-item label="评分">{{ day.hotel.rating }}⭐</a-descriptions-item>
                  <a-descriptions-item label="距离" :span="2">{{ day.hotel.distance }}</a-descriptions-item>
                </a-descriptions>
              </a-card>

              <!-- 餐饮安排 -->
              <a-divider orientation="left">🍽️ 餐饮安排</a-divider>
              <a-descriptions :column="1" bordered size="small">
                <a-descriptions-item v-for="meal in day.meals" :key="meal.type" :label="getMealLabel(meal.type)">
                  {{ meal.name }}
                  <span v-if="meal.description"> - {{ meal.description }}</span>
                </a-descriptions-item>
              </a-descriptions>
            </a-collapse-panel>
          </a-collapse>
        </a-card>
  </div>
</template>

<script setup lang="ts">
console.log('✅ trvlEdit mounted')
import { ref, onMounted } from 'vue'
import {message} from "ant-design-vue";

const tripPlan = ref<any>(null)
const activeDays = ref<number[]>([0]) // 默认展开第一天
const getMealLabel = (type: string): string => {
  const labels: Record<string, string> = {
    breakfast: '早餐',
    lunch: '午餐',
    dinner: '晚餐',
    snack: '小吃'
  }
  return labels[type] || type
}




onMounted(() => {
  const raw = sessionStorage.getItem('tripPlan')
  if (raw) {
    tripPlan.value = JSON.parse(raw)
    console.log('trvlEdit 拿到数据:', tripPlan.value)
  } else {
    // 没有数据，提示用户回首页填写
    message.warning('暂无旅行计划数据，请先在首页生成')
  }
})



// 景点图片处理
const getAttractionImage = (name: string, index: number): string => {
  // 如果已加载真实图片,返回真实图片
  if (attractionPhotos.value[name]) {
    return attractionPhotos.value[name]
  }

  // 返回一个纯色占位图(避免跨域问题)
  const colors = [
    { start: '#667eea', end: '#764ba2' },
    { start: '#f093fb', end: '#f5576c' },
    { start: '#4facfe', end: '#00f2fe' },
    { start: '#43e97b', end: '#38f9d7' },
    { start: '#fa709a', end: '#fee140' }
  ]
  const colorIndex = index % colors.length
  const { start, end } = colors[colorIndex]

  // 使用base64编码避免中文问题
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300">
    <defs>
      <linearGradient id="grad${index}" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:${start};stop-opacity:1" />
        <stop offset="100%" style="stop-color:${end};stop-opacity:1" />
      </linearGradient>
    </defs>
    <rect width="400" height="300" fill="url(#grad${index})"/>
    <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="24" font-weight="bold" fill="white">${name}</text>
  </svg>`

  return `data:image/svg+xml;base64,${btoa(unescape(encodeURIComponent(svg)))}`
}

// 图片加载失败时的处理
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  // 使用灰色占位图
  img.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="400" height="300"%3E%3Crect width="400" height="300" fill="%23f0f0f0"/%3E%3Ctext x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="18" fill="%23999"%3E图片加载失败%3C/text%3E%3C/svg%3E'
}


</script>

<!-- 不要留下空的style scoped!!!!!会报错 -->