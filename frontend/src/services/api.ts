import axios from 'axios'
import type { TripFormData, TripPlanResponse, PoiResult,PoiResponse} from '@/types'

// api基础地址
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// 创建axios实例
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5分钟超时
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    console.log('发送请求:', config.method?.toUpperCase(), config.url)
    return config
  },
  (error) => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    console.log('收到响应:', response.status, response.config.url)
    return response
  },
  (error) => {
    console.error('响应错误:', error.response?.status, error.message)
    return Promise.reject(error)
  }
)

/**
 * 生成旅行计划
 */
export async function generateTripPlan(formData: TripFormData): Promise<TripPlanResponse> {
  try {
    const response = await apiClient.post<TripPlanResponse>('/api/trip/plan', formData)
    return response.data  // axios把json解析后放在.data里    ↑ ↑ ↑ 意思是说，返回的类型为TripPlanResponse。
  } catch (error: any) {
    console.error('生成旅行计划失败:', error)
    throw new Error(error.response?.data?.detail || error.message || '生成旅行计划失败')
  }
}

/**
 * 健康检查
 */
export async function healthCheck(): Promise<any> {
  try {
    const response = await apiClient.get('/health')
    return response.data
  } catch (error: any) {
    console.error('健康检查失败:', error)
    throw new Error(error.message || '健康检查失败')
  }
}


// =============================尝试适配MapShow部分的新增poi=========================================

/**
 * 【新增】搜索POI
 * 意义：mapshow.vue 页面调用此函数，将搜索关键词传给后端，
 *       后端通过高德MCP服务获取POI数据后返回给前端渲染地图
 */
export async function searchPoi(keywords: string, city: string = '北京'): Promise<PoiResponse> {
  try {
    const response = await apiClient.get<PoiResponse>('api/map/poi', {
      params: { keywords, city },
    })
    return response.data
  } catch (error: any) {
    console.error('POI搜索失败:', error)
    throw new Error(error.response?.data?.detail || error.message || 'POI搜索失败')
  }
}

/**
 * 【新增】获取MCP工具列表（调试用）
 * 意义：开发阶段可在页面中查看所有可用的MCP工具名称和描述，
 *       方便确认后端MCP连接是否正常
 */
export async function getMcpTools(): Promise<any> {
  try {
    const response = await apiClient.get('api/map/tools')
    return response.data
  } catch (error: any) {
    console.error('获取MCP工具列表失败:', error)
    throw new Error(error.message || '获取MCP工具列表失败')
  }
}

// ======================== 新增结束 ========================


