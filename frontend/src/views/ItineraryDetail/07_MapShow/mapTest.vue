<!-- src/views/mapshow.vue -->
<template>
  <a-layout class="map-page">
    <!-- 顶部搜索栏 -->
    <a-layout-header class="map-header">
      <div class="header-content">
        <h2 class="title">🗺️ 地点搜索：</h2>
        <a-input-search
          v-model:value="searchKeyword"
          placeholder="搜索地点，如：咖啡、景点..."
          enter-button="搜索"
          size="large"
          class="search-input"
          :loading="loading"
          @search="handleSearch"
        />
        <a-select
          v-model:value="selectedCity"
          class="city-select"
          size="large"
        >
          <a-select-option value="北京">北京</a-select-option>
          <a-select-option value="上海">上海</a-select-option>
          <a-select-option value="广州">广州</a-select-option>
          <a-select-option value="深圳">深圳</a-select-option>
          <a-select-option value="杭州">杭州</a-select-option>
          <a-select-option value="成都">成都</a-select-option>
        </a-select>
      </div>
    </a-layout-header>

    <a-layout-content class="map-body">
      <!-- 左半部分：地图 -->
      <div class="map-left">
        <div id="amap-container" class="map-container"></div>

        <!-- 加载状态覆盖 -->
        <div v-if="loading" class="map-loading">
          <a-spin size="large" tip="搜索中..." />
        </div>

        <!-- 搜索结果列表浮层 -->
        <div v-if="poiList.length > 0" class="poi-panel">
          <a-list
            size="small"
            :data-source="poiList"
            :pagination="{ pageSize: 5, size: 'small' }"
          >
            <template #renderItem="{ item }">
              <a-list-item @click="focusPoi(item)" class="poi-item">
                <a-list-item-meta>
                  <template #title>
                    <span class="poi-name">{{ item.name }}</span>
                  </template>
                  <template #description>
                    <span class="poi-address">{{ item.address || '暂无地址' }}</span>
                  </template>
                </a-list-item-meta>
              </a-list-item>
            </template>
          </a-list>
        </div>
      </div>

      <!-- 右半部分：空白预留 -->
      <div class="map-right">
        <a-empty description="预留区域（可扩展为详情面板）" />
      </div>
    </a-layout-content>
  </a-layout>
</template>


<script setup lang="ts" >
import {ref, onMounted, onUnmounted, onActivated, nextTick,} from 'vue'
import AMapLoader from '@amap/amap-jsapi-loader'
import { searchPoi } from '@/services/api.ts'
import { message } from 'ant-design-vue'

// ==================== 状态 ====================
const searchKeyword = ref('')
const selectedCity = ref('北京')
const loading = ref(false)
const poiList = ref<any[]>([])


let mapInstance: any = null
let markers: any[] = []
let AMapRef: any = null          // ✅ 新增：保存 AMap 引用供全局使用


const currentMarker = ref(null) // ✅ 保存当前标记引用，避免重复创建
// ==================== 地图初始化 ====================
onMounted(async () => {
  try {
    const AMap = await AMapLoader.load({
      //key: '你的高德Web端JS API Key',  // 注意：这里用的是JS API Key，不是MCP的key
      key: import.meta.env.VITE_AMAP_WEB_JS_KEY,  // 注意：这里用的是JS API Key，不是MCP的key
      version: '2.0',
      plugins: ['AMap.PlaceSearch', 'AMap.Marker'],
    })

    AMapRef = AMap              // ✅ 新增：保存到模块级变量

    mapInstance = new AMap.Map('amap-container', {
      zoom: 12,
      center: [116.397428, 39.90923], // 默认北京中心
      viewMode: '2D',
    })

    console.log('✅ 地图初始化成功')
    // await initMapSafely()
  } catch (e) {
    console.error('❌ 地图加载失败:', e)
    message.error('地图加载失败，请检查网络或Key配置')
  }
})

onUnmounted(() => {
  // 销毁地图实例，防止内存泄漏
  if (mapInstance) {
    mapInstance.destroy()
    mapInstance = null
  }
})

// ==================== 搜索逻辑 ====================
async function handleSearch() {
  if (!searchKeyword.value.trim()) {
    message.warning('请输入搜索关键词')
    return
  }

  loading.value = true
  poiList.value = []

  try {
    // 调用后端接口 → 后端调用高德MCP
    const res = await searchPoi(searchKeyword.value, selectedCity.value)

    if (res.success && res.data) {
      // 解析MCP返回的数据（根据实际结构适配）
      const rawPois = parsePoiData(res.data)
      poiList.value = rawPois
      renderMarkers(rawPois)
      message.success(`找到 ${rawPois.length} 个结果`)
    } else {
      message.warning(res.message || '未找到结果')
    }
  } catch (e: any) {
    message.error(e.message || '搜索失败')
  } finally {
    loading.value = false
  }
}

/**
 * 解析MCP返回的POI数据
 * 根据高德MCP实际返回格式进行适配
 */
function parsePoiData(data: any): any[] {
  // 如果返回的是字符串，尝试JSON解析
  let parsed = data
  if (typeof data === 'string') {
    try {
      parsed = JSON.parse(data)
    } catch {
      return []
    }
  }

  // 高德POI搜索通常返回 { pois: [...] }
  if (parsed?.pois?.poi) {
    return parsed.pois.poi
  }
  if (Array.isArray(parsed?.pois)) {
    return parsed.pois
  }
  if (Array.isArray(parsed)) {
    return parsed
  }

  console.warn('未识别的POI数据结构:', parsed)
  return []
}


// ==================== 地图打点 ====================
function renderMarkers(pois: any[]) {
  if (!mapInstance) return

  // 清除旧标记
  clearMarkers()

  const AMap = (window as any).AMap

  pois.forEach((poi: any, index: number) => {
    // 解析坐标 "116.397,39.909" → [116.397, 39.909]
    let lnglat: [number, number] | null = null

    if (poi.location) {
      const [lng, lat] = poi.location.split(',').map(Number)
      if (!isNaN(lng) && !isNaN(lat)) {
        lnglat = [lng, lat]
      }
    }

    if (!lnglat) return

    const marker = new AMap.Marker({
      position: lnglat,
      title: `${index + 1}. ${poi.name}`,
      label: {
        content: `<div class="marker-label">${poi.name}</div>`,
        direction: 'top',
      },
    })

    // 点击标记显示信息窗
    marker.on('click', () => {
      const infoWindow = new AMap.InfoWindow({
        content: `
          <div style="padding:8px;max-width:250px;">
            <h4 style="margin:0 0 4px">${poi.name}</h4>
            <p style="margin:0;color:#666;font-size:12px">${poi.address || ''}</p>
            ${poi.tel ? `<p style="margin:4px 0 0;font-size:12px">📞 ${poi.tel}</p>` : ''}
          </div>
        `,
        offset: new AMap.Pixel(0, -30),
      })
      infoWindow.open(mapInstance, lnglat)
    })

    markers.push(marker)
    mapInstance.add(marker)
  })

  // 自动调整视野以包含所有标记
  if (markers.length > 0) {
    mapInstance.setFitView(markers)
  }
}

function clearMarkers() {
  markers.forEach((m) => m.remove?.() || mapInstance.remove(m))
  markers = []
}

// 点击列表项定位到对应标记
function focusPoi(poi: any) {
  // 重写版本
  if (!mapInstance || !AMapRef) return

  // ✅ 统一坐标解析逻辑（与 renderMarkers 保持一致）
  let lng: number, lat: number
  if (typeof poi.location === 'string') {
    const parts = poi.location.split(',').map(Number)
    lng = parts[0]
    lat = parts[1]
  } else if (poi.location?.longitude != null) {
    lng = poi.location.longitude
    lat = poi.location.latitude
  } else {
    console.warn('无法解析POI坐标:', poi)
    return
  }

  if (isNaN(lng) || isNaN(lat)) return

  // ✅ mapInstance 是普通变量，不要加 .value
  mapInstance.setZoomAndCenter(16, [lng, lat])

  // 清除旧的水滴标记
  if (currentMarker.value) {
    mapInstance.remove(currentMarker.value)
    currentMarker.value = null
  }

  // ✅ 使用 AMapRef 代替不存在的 AMap
  currentMarker.value = new AMapRef.Marker({
    position: [lng, lat],
    title: poi.name,
    icon: new AMapRef.Icon({
      size: new AMapRef.Size(25, 34),
      image: 'https://webapi.amap.com/theme/v1.3/markers/n/mark_b.png',
      imageSize: new AMapRef.Size(25, 34),
    }),
    // offset: new AMapRef.Pixel(-12, -34), // 尝试删除偏移
    anchor: 'bottom-center',
  })

  mapInstance.add(currentMarker.value)
}


/**
 * 对当前地点进行简单标记
 * 倒置的水滴形状。
 */
function setMarker(lng, lat, title = '') {
  if (!mapInstance || !AMapRef) return

  if (currentMarker.value) {
    mapInstance.remove(currentMarker.value)
    currentMarker.value = null
  }

  currentMarker.value = new AMapRef.Marker({
    position: [lng, lat],
    title: title,
    icon: new AMapRef.Icon({
      size: new AMapRef.Size(25, 34),
      image: 'https://webapi.amap.com/theme/v1.3/markers/n/mark_b.png',
      imageSize: new AMapRef.Size(25, 34),
    }),
    offset: new AMapRef.Pixel(-12, -34),
    anchor: 'bottom-center',
  })

  mapInstance.add(currentMarker.value)
}

</script>

<style scoped>
.map-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.map-header {
  background: #fff;
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  z-index: 10;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 16px;
  height: 64px;
}

.title {
  margin: 0;
  font-size: 18px;
  white-space: nowrap;
}

.search-input {
  width: 320px;
}

.city-select {
  width: 120px;
}

/* ===== 核心布局：左右各50% ===== */
.map-body {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.map-left {
  width: 50%;
  height: 100%;
  position: relative;
}

.map-container {
  width: 100%;
  height: 100%;
}

.map-right {
  width: 50%;
  height: 100%;
  background: #fafafa;
  border-left: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 加载遮罩 */
.map-loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

/* POI结果浮层 */
.poi-panel {
  position: absolute;
  top: 12px;
  left: 12px;
  width: 280px;
  max-height: 400px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  overflow-y: auto;
  z-index: 50;
}

.poi-item {
  cursor: pointer;
  transition: background 0.2s;
}

.poi-item:hover {
  background: #e6f7ff;
}

.poi-name {
  font-weight: 500;
  color: #333;
}

.poi-address {
  font-size: 12px;
  color: #999;
}
</style>