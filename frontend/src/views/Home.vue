<template>
  <div class="home-container">
    <!-- 背景装饰 -->
    <div class="bg-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>

    <!-- 页面标题 -->
    <div class="page-header">
      <div class="icon-wrapper">
        <span class="icon">✈️</span>
      </div>
      <h1 class="page-title">刚生没几天的TravelAgent</h1>
      <p class="page-subtitle">不知道什么AI，也不知道什么旅游规划。偷猪3缺1哦</p>
    </div>

    <a-card class="form-card" :bordered="false">
      <a-form :model="formData" layout="vertical" @finish="handleSubmit">

        <!--jlq_add: 分左右的新增盒子-->
        <div class="card-container">

          <div class="form-section"><!--左边去！-->
            <div class="section-header">
              <span class="section-icon">🍭</span>
              <span class="section-title">出游时间设置</span>
            </div>

            <!--            <a-col :span="8">-->
            <!--              <a-form-item name="city" :rules="[{ required: true, message: '请输入目的地城市' }]">-->
            <!--                <template #label>-->
            <!--                  <span class="form-label">目的地城市</span>-->
            <!--                </template>-->
            <!--                <a-input-->
            <!--                  v-model:value="formData.city"-->
            <!--                  placeholder="例如: 北京"-->
            <!--                  size="large"-->
            <!--                  class="custom-input"-->
            <!--                >-->
            <!--                  <template #prefix>-->
            <!--                    <span style="color: #1890ff;">🏙️</span>-->
            <!--                  </template>-->
            <!--                </a-input>-->
            <!--              </a-form-item>-->
            <!--            </a-col>-->

            <a-row :gutter="24">
              <a-col :span="6">
                <a-form-item name="start_date" :rules="[{ required: true, message: '请选择开始日期' }]">
                  <template #label>
                    <span class="form-label">开始日期</span>
                  </template>
                  <a-date-picker v-model:value="formData.start_date" style="width: 100%" size="large"
                    class="custom-input" placeholder="选择日期" />
                </a-form-item>
              </a-col>



              <!-- 可选项：具体开始时间 -->
              <a-col :span="6">
                <a-form-item name="start_date">
                  <template #label>
                    <span class="form-label">具体开始时间</span>
                  </template>
                    <a-space direction="vertical">
                      <a-time-picker v-model:value="value"  style="width: 100%" size="large"/>
                    </a-space>
                </a-form-item>
              </a-col>
            </a-row>
            

            <a-row :gutter="24">
              <a-col :span="6">
                <a-form-item name="end_date" :rules="[{ required: true, message: '请选择结束日期' }]">
                  <template #label>
                    <span class="form-label">结束日期</span>
                  </template>
                  <a-date-picker v-model:value="formData.end_date" style="width: 100%" size="large" class="custom-input"
                    placeholder="选择日期" />
                </a-form-item>
              </a-col>

              <!-- 可选项：具体结束时间 -->
              <a-col :span="6">
                <a-form-item name="end_date">
                  <template #label>
                    <span class="form-label">具体结束时间</span>
                  </template>
                    <a-space direction="vertical">
                      <a-time-picker v-model:value="strValue" value-format="HH:mm:ss" style="width: 100%" size="large" />
                    </a-space>
                </a-form-item>
              </a-col>
            </a-row>


            <a-row :gutter="24">
              <a-col :span="4">
                <a-form-item>
                  <template #label>
                    <span class="form-label">旅行天数合计</span>
                  </template>
                  <div class="days-display-compact">
                    <span class="days-value">{{ formData.travel_days }}</span>
                    <span class="days-unit">天</span>
                  </div>
                </a-form-item>
              </a-col>
            </a-row>
          </div><!--第一行，左方标记卡结束-->

          <!-- jlq_add : 第一行，右方标记卡开始 -->
          <div class="form-section">
            <div class="section-header">
              <span class="section-icon">📍</span>
              <span class="section-title">私有事务标记</span>
            </div>
            
            <!-- 各类杂项选择 -->
                     <a-row :gutter="24">
                       <a-col :span="8">
                         <a-form-item name="transportation">
                           <template #label>
                             <span class="form-label">交通方式</span>
                           </template>
                           <a-select v-model:value="formData.transportation" size="large" class="custom-select">
                             <a-select-option value="公共交通">🚇 公共交通</a-select-option>
                             <a-select-option value="自驾">🚗 自驾</a-select-option>
                             <a-select-option value="步行">🚶 步行</a-select-option>
                             <a-select-option value="混合">🔀 混合</a-select-option>
                           </a-select>
                         </a-form-item>
                       </a-col>
                       <a-col :span="8">
                         <a-form-item name="accommodation">
                           <template #label>
                             <span class="form-label">住宿偏好</span>
                           </template>
                           <a-select v-model:value="formData.accommodation" size="large" class="custom-select">
                             <a-select-option value="经济型酒店">💰 经济型酒店</a-select-option>
                             <a-select-option value="舒适型酒店">🏨 舒适型酒店</a-select-option>
                             <a-select-option value="豪华酒店">⭐ 豪华酒店</a-select-option>
                             <a-select-option value="民宿">🏡 民宿</a-select-option>
                           </a-select>
                         </a-form-item>
                       </a-col>
                       <a-col :span="8">
                         <a-form-item name="preferences">
                           <template #label>
                             <span class="form-label">修改权限开放</span>
                           </template>
                           <div class="preference-tags">
                             <a-checkbox-group v-model:value="formData.preferences" class="custom-checkbox-group">
                               <a-checkbox value="自然风光" class="preference-tag">🏞️ 景点</a-checkbox>
                               <a-checkbox value="美食" class="preference-tag">🍜 吃饭</a-checkbox>
                               <a-checkbox value="购物" class="preference-tag">🛍️ 住宿</a-checkbox>
                               <a-checkbox value="艺术" class="preference-tag">🎨 前置事项</a-checkbox>
                               <a-checkbox value="休闲" class="preference-tag">☕ 特别活动</a-checkbox>
                             </a-checkbox-group>
                           </div>
                         </a-form-item>
                       </a-col>
                     </a-row>


            <!-- 大输入框 -->
            <a-form-item name="free_text_input">
              <a-textarea v-model:value="formData.free_text_input" placeholder="请输入您的额外要求,例如:想去看升旗、需要无障碍设施、对海鲜过敏等..."
                :rows="3" size="large" class="custom-textarea" />
            </a-form-item>
          </div>

        </div><!-- jlq_add : 第一行，右方标记卡结束 -->


        <!--第二行分板开始-->
        <div class="card-container">
          <!-- 第二步:偏好设置 -->
          <div class="form-section">
            <div class="section-header">
              <span class="section-icon">⚙️</span>
              <span class="section-title">策划组</span>
            </div>

            <!--jlq_add: 策划组列表页面-->
            <PlanningTeamForm />
          </div>
          
          <!-- 第二行，右方分板开始 -->
          <div class="form-section">
            <div class="section-header">
              <span class="section-icon">🎡</span>
              <span class="section-title">参与组</span>
            </div>

            <!--jlq_add: 参与组列表页面-->
            <ParticipatingTeamForm />
          </div>

        </div><!--第二行分板结束-->

        <!-- 第三行单板，更新说明 -->
        <div class="form-section">
          <div class="section-header">
            <span class="section-icon">🌟</span>
            <span class="section-title">行程计划更新说明</span>
          </div>

          <!-- 标签页，装载计划更新说明 -->
              <div class="card-container">
                <a-tabs v-model:activeKey="activeKey" type="card" size = "large" >
                  <a-tab-pane key="1" tab="前置活动" >
                    <!-- <p>我观阁下这位阁下那位阁下全都很有姿色，我的我的都是我的全是我的嘿嘿一个也别想跑</p>
                    <p>Content of Tab Pane 1</p>
                    <p>Content of Tab Pane 1</p> -->

                    <!-- 修改为卡片展示 -->
                    
                      <!-- 卡片展示结束 -->

                  </a-tab-pane>
                  <a-tab-pane key="2" tab="特别活动">
                    <p>Content of Tab Pane 2</p>
                    <p>Content of Tab Pane 2</p>
                    <p>Content of Tab Pane 2</p>
                  </a-tab-pane>
                  <a-tab-pane key="3" tab="旅途计划">
                    <p>Content of Tab Pane 3</p>
                    <p>Content of Tab Pane 3</p>
                    <p>Content of Tab Pane 3</p>
                  </a-tab-pane>
                </a-tabs>
              </div>
        </div><!-- 行程计划更新说明结束 -->

        <!-- 提交按钮 -->
        <a-form-item>
          <a-button type="primary" html-type="submit" :loading="loading" size="large" block class="submit-button">
            <template v-if="!loading">
              <span class="button-icon">🚀</span>
              <span>查看详细内容</span>
            </template>
            <template v-else>
              <span>正在拉取中...</span>
            </template>
          </a-button>
        </a-form-item>

        <!-- 加载进度条 -->
        <a-form-item v-if="loading">
          <div class="loading-container">
            <a-progress :percent="loadingProgress" status="active" :stroke-color="{
              '0%': '#667eea',
              '100%': '#764ba2',
            }" :stroke-width="10" />
            <p class="loading-status">
              {{ loadingStatus }}
            </p>
          </div>
        </a-form-item>
      </a-form>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { generateTripPlan } from '@/services/api.ts'
import type { TripFormData } from '@/types'
import type { Dayjs } from 'dayjs'
import dayjs from 'dayjs'

// jlq_add : 新增组件页面 //
import PlanningTeamForm from './Home_PlanningTeamForm.vue'
import ParticipatingTeamForm from './Home_PtcpTeamForm.vue'
// jlq_add END //

const router = useRouter()
const loading = ref(false)
const loadingProgress = ref(0)
const loadingStatus = ref('')

// 更新说明所需要用的变量=======
const activeKey = ref('2');
//============================


// 面板1 可选项 开始 & 结束时刻 ======
const value = ref<Dayjs>(dayjs('08:00:00', 'HH:mm:ss'));
const strValue = ref<string>('09:00:00');
// =================================

const formData = reactive<TripFormData & { start_date: Dayjs | null; end_date: Dayjs | null }>({
  city: '',
  start_date: null,
  end_date: null,
  travel_days: 1,
  transportation: '公共交通',
  accommodation: '经济型酒店',
  preferences: [],
  free_text_input: ''
})


// 监听日期变化,自动计算旅行天数
watch([() => formData.start_date, () => formData.end_date], ([start, end]) => {
  if (start && end) {
    const days = end.diff(start, 'day') + 1
    if (days > 0 && days <= 30) {
      formData.travel_days = days
    } else if (days > 30) {
      message.warning('旅行天数不能超过30天')
      formData.end_date = null
    } else {
      message.warning('结束日期不能早于开始日期')
      formData.end_date = null
    }
  }
})

const handleSubmit = async () => {
  if (!formData.start_date || !formData.end_date) {
    message.error('请选择日期')
    return
  }

  loading.value = true
  loadingProgress.value = 0
  loadingStatus.value = '正在初始化...'

  // 模拟进度更新
  const progressInterval = setInterval(() => {
    if (loadingProgress.value < 90) {
      loadingProgress.value += 10

      // 更新状态文本
      if (loadingProgress.value <= 30) {
        loadingStatus.value = '🔍 正在搜索景点...'
      } else if (loadingProgress.value <= 50) {
        loadingStatus.value = '🌤️ 正在查询天气...'
      } else if (loadingProgress.value <= 70) {
        loadingStatus.value = '🏨 正在推荐酒店...'
      } else {
        loadingStatus.value = '📋 正在生成行程计划...'
      }
    }
  }, 500)

  try {
    const requestData: TripFormData = {
      city: formData.city,
      start_date: formData.start_date.format('YYYY-MM-DD'),
      end_date: formData.end_date.format('YYYY-MM-DD'),
      travel_days: formData.travel_days,
      transportation: formData.transportation,
      accommodation: formData.accommodation,
      preferences: formData.preferences,
      free_text_input: formData.free_text_input
    }

    const response = await generateTripPlan(requestData)

    clearInterval(progressInterval)
    loadingProgress.value = 100
    loadingStatus.value = '✅ 完成!'

    if (response.success && response.data) {
      // 保存到sessionStorage
      sessionStorage.setItem('tripPlan', JSON.stringify(response.data))

      message.success('旅行计划生成成功!')

      // 短暂延迟后跳转
      setTimeout(() => {
        router.push('/result')
      }, 500)
    } else {
      message.error(response.message || '生成失败')
    }
  } catch (error: any) {
    clearInterval(progressInterval)
    message.error(error.message || '生成旅行计划失败,请稍后重试')
  } finally {
    setTimeout(() => {
      loading.value = false
      loadingProgress.value = 0
      loadingStatus.value = ''
    }, 1000)
  }

  // // 面板1 可选项 开始 & 结束时刻
  watch(value, () => {
    console.log(value.value);
  });
  watch(strValue, () => {
    console.log(strValue.value);
  });

  
}

// jlq_add // 新增用户列表部分变量


// jlq_add END //


</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60px 20px;
  position: relative;
  overflow: hidden;
}

/* 背景装饰 */
.bg-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
}

.circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 20s infinite ease-in-out;
}

.circle-1 {
  width: 300px;
  height: 300px;
  top: -100px;
  left: -100px;
  animation-delay: 0s;
}

.circle-2 {
  width: 200px;
  height: 200px;
  top: 50%;
  right: -50px;
  animation-delay: 5s;
}

.circle-3 {
  width: 150px;
  height: 150px;
  bottom: -50px;
  left: 30%;
  animation-delay: 10s;
}

@keyframes float {

  0%,
  100% {
    transform: translateY(0) rotate(0deg);
  }

  50% {
    transform: translateY(-30px) rotate(180deg);
  }
}

/* 页面标题 */
.page-header {
  text-align: center;
  margin-bottom: 50px;
  animation: fadeInDown 0.8s ease-out;
  position: relative;
  z-index: 1;
}

.icon-wrapper {
  margin-bottom: 20px;
}

.icon {
  font-size: 80px;
  display: inline-block;
  animation: bounce 2s infinite;
}

@keyframes bounce {

  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-20px);
  }
}

.page-title {
  font-size: 56px;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 16px;
  text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
  letter-spacing: 2px;
}

.page-subtitle {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.95);
  margin: 0;
  font-weight: 300;
}

/* 表单卡片 */
.form-card {
  max-width: 1700px;
  /* 维持整个页面卡片的人形 */
  margin: 0 auto;
  border-radius: 24px;
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.4);
  animation: fadeInUp 0.8s ease-out;
  position: relative;
  z-index: 1;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.98) !important;
}

/* 表单分区 */
.form-section {
  margin-bottom: 32px;
  padding: 24px;
  background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
  border-radius: 16px;
  border: 1px solid #e8e8e8;
  transition: all 0.3s ease;

  /* jlq_add：出游时间设置，将其放置到左边 */
  flex: 1;
  /* 核心修改！让它自动占据可用空间 */
  /* 删掉原来的 max-width: 1400px; */
  margin: 0;
  /* 原来有 margin: 0 auto，现在交给外层容器控制居中，所以这里设为0 */
  position: relative;
}

.form-section:hover {
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
  transform: translateY(-2px);
}

.section-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #667eea;
}

.section-icon {
  font-size: 24px;
  margin-right: 12px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

/* 表单标签 */
.form-label {
  font-size: 15px;
  font-weight: 500;
  color: #555;
}

/* 自定义输入框 */
.custom-input :deep(.ant-input),
.custom-input :deep(.ant-picker) {
  border-radius: 12px;
  border: 2px solid #e8e8e8;
  transition: all 0.3s ease;
}

.custom-input :deep(.ant-input:hover),
.custom-input :deep(.ant-picker:hover) {
  border-color: #667eea;
}

.custom-input :deep(.ant-input:focus),
.custom-input :deep(.ant-picker-focused) {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* 自定义选择框 */
.custom-select :deep(.ant-select-selector) {
  border-radius: 12px !important;
  border: 2px solid #e8e8e8 !important;
  transition: all 0.3s ease;
}

.custom-select:hover :deep(.ant-select-selector) {
  border-color: #667eea !important;
}

.custom-select :deep(.ant-select-focused .ant-select-selector) {
  border-color: #667eea !important;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

/* 天数显示 - 紧凑版 */
.days-display-compact {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  padding: 8px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
}

.days-display-compact .days-value {
  font-size: 24px;
  font-weight: 700;
  margin-right: 4px;
}

.days-display-compact .days-unit {
  font-size: 14px;
}

/* 偏好标签 */
.preference-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.custom-checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  width: 100%;
}

.preference-tag :deep(.ant-checkbox-wrapper) {
  margin: 0 !important;
  padding: 8px 16px;
  border: 2px solid #e8e8e8;
  border-radius: 20px;
  transition: all 0.3s ease;
  background: white;
  font-size: 14px;
}

.preference-tag :deep(.ant-checkbox-wrapper:hover) {
  border-color: #667eea;
  background: #f5f7ff;
}

.preference-tag :deep(.ant-checkbox-wrapper-checked) {
  border-color: #667eea;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

/* 自定义文本域 */
.custom-textarea :deep(.ant-input) {
  border-radius: 12px;
  border: 2px solid #e8e8e8;
  transition: all 0.3s ease;
}

.custom-textarea :deep(.ant-input:hover) {
  border-color: #667eea;
}

.custom-textarea :deep(.ant-input:focus) {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* 提交按钮 */
.submit-button {
  height: 56px;
  border-radius: 28px;
  font-size: 18px;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
}

.submit-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.5);
}

.submit-button:active {
  transform: translateY(0);
}

.button-icon {
  margin-right: 8px;
  font-size: 20px;
}

/* 加载容器 */
.loading-container {
  text-align: center;
  padding: 24px;
  background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
  border-radius: 16px;
  border: 2px dashed #667eea;
}

.loading-status {
  margin-top: 16px;
  color: #667eea;
  font-size: 18px;
  font-weight: 500;
}

/* 动画 */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* jlq_add : 两行的左右盒子*/
.card-container {
  display: flex;
  /* 开启弹性盒子，让子元素左右排列 */
  gap: 24px;
  /* 两个卡片之间的间距 */
  max-width: 1920px;
  /* 限制整个并排区域的最大宽度，你可以自己调 */
  margin: 0 auto;
  /* 让这一整块内容在页面里居中 */
}


/* 以下是 计划更新说明的标签页 */
.card-container p {
  margin: 0;
}
.card-container > .ant-tabs-card .ant-tabs-content {
  height: 120px;
  margin-top: -16px;
}
.card-container > .ant-tabs-card .ant-tabs-content > .ant-tabs-tabpane {
  padding: 16px;
  background: #fff;
}
.card-container > .ant-tabs-card > .ant-tabs-nav::before {
  display: none;
}
.card-container > .ant-tabs-card .ant-tabs-tab,
[data-theme='compact'] .card-container > .ant-tabs-card .ant-tabs-tab {
  background: transparent;
  border-color: transparent;
}
.card-container > .ant-tabs-card .ant-tabs-tab-active,
[data-theme='compact'] .card-container > .ant-tabs-card .ant-tabs-tab-active {
  background: #fff;
  border-color: #fff;
}
#components-tabs-demo-card-top .code-box-demo {
  padding: 24px;
  overflow: hidden;
  background: #f5f5f5;
}
[data-theme='compact'] .card-container > .ant-tabs-card .ant-tabs-content {
  height: 120px;
  margin-top: -8px;
}
[data-theme='dark'] .card-container > .ant-tabs-card .ant-tabs-tab {
  background: transparent;
  border-color: transparent;
}
[data-theme='dark'] #components-tabs-demo-card-top .code-box-demo {
  background: #000;
}
[data-theme='dark'] .card-container > .ant-tabs-card .ant-tabs-content > .ant-tabs-tabpane {
  background: #141414;
}
[data-theme='dark'] .card-container > .ant-tabs-card .ant-tabs-tab-active {
  background: #141414;
  border-color: #141414;
}


</style>
