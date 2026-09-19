import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface TripPoint {
  id: string          // POI 唯一 id，用于 diff
  name: string
  lng: number
  lat: number
  dayIndex?: number   // 属于第几天
}

export const useTripMarkerStore = defineStore('tripMarker', () => {
  const points = ref<TripPoint[]>([])   // trvlEdit 指向的地点列表
  const dirty = ref(true)               // ✅ 脏标记：数据变化时置 true

  // 生成一个"指纹"，用于精确判断内容是否真的变了（可选的二次保险）
  const fingerprint = computed(() =>
    points.value.map(p => `${p.id}:${p.lng},${p.lat}`).join('|')
  )

  /** trvlEdit 调用：更新行程地点 */
  function updatePoints(newPoints: TripPoint[]) {
    const newFp = newPoints.map(p => `${p.id}:${p.lng},${p.lat}`).join('|')
    if (newFp === fingerprint.value) return   // 内容没变，不触发 dirty
    points.value = newPoints
    dirty.value = true
  }

  /** mapTest 调用：消费完数据后重置脏标记 */
  function consume() {
    dirty.value = false
  }

  return { points, dirty, fingerprint, updatePoints, consume }
})