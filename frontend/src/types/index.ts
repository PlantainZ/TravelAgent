// 类型定义

export interface Location {
  longitude: number
  latitude: number
}

export interface Attraction {
  name: string
  address: string
  location: Location
  visit_duration: number
  description: string
  category?: string
  rating?: number
  image_url?: string
  ticket_price?: number
}

export interface Meal {
  type: 'breakfast' | 'lunch' | 'dinner' | 'snack'
  name: string
  address?: string
  location?: Location
  description?: string
  estimated_cost?: number
}

export interface Hotel {
  name: string
  address: string
  location?: Location
  price_range: string
  rating: string
  distance: string
  type: string
  estimated_cost?: number
}

export interface Budget {
  total_attractions: number
  total_hotels: number
  total_meals: number
  total_transportation: number
  total: number
}

export interface DayPlan {
  date: string
  day_index: number
  description: string
  transportation: string
  accommodation: string
  hotel?: Hotel
  attractions: Attraction[]
  meals: Meal[]
}

export interface WeatherInfo {
  date: string
  day_weather: string
  night_weather: string
  day_temp: number
  night_temp: number
  wind_direction: string
  wind_power: string
}

export interface TripPlan {
  city: string
  start_date: string
  end_date: string
  days: DayPlan[]
  weather_info: WeatherInfo[]
  overall_suggestions: string
  budget?: Budget
}

export interface TripFormData {
  city: string
  start_date: string
  end_date: string
  travel_days: number
  transportation: string
  accommodation: string
  preferences: string[]
  free_text_input: string
}

export interface TripPlanResponse {
  success: boolean
  message: string
  data?: TripPlan
}

// B_ItemList.vue 所用数据清单 ===================================

// 枚举
/** 物品重要性 */
export enum Importance {
  Important = 'important',
  Unimportant = 'unimportant',
}
/** 物品任务是否已完成 */
export enum isDone{
  Done = 'yes',
  notDone = 'no',
}


// 接口
/** 单个物品 */
export interface Item {
  /** 新增：物品序号 */
  key:string
  /** 物品名称 */
  name: string
  /** 重要性 */
  importance: Importance
  /** 物品备注 */
  remark: string
   /** 是否已经买到，或者拥有？ */
  itemState?: isDone
}

/** 物品类别（如：药品、食品、生活用品） */
export interface Category {
  /** 类别名称 */
  name: string
  /** 类别备注 */
  remark: string
  /** 该类别下的所有物品 */
  items: Item[]
}

/** 整个所需物品清单 */
export interface ShoppingList {
  /** 清单标题 */
  title: string
  /** 创建时间（可选） */
  createdAt?: string
  /** 所有类别 */
  categories: Category[]
}
