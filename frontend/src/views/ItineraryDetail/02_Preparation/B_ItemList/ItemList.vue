<template>
  <div>

    <h3> This is ITEMlist!!!!!!!!!!!!!!!!!!!!!!!!oooooo</h3>

    <!-- 基础物品列表 -->

    <div>
      <a-radio-group v-model:value="viewMode" :style="{ marginBottom: '8px' }">
        <a-radio-button value="travel">旅游前置</a-radio-button>
        <a-radio-button value="local">当地特色推荐</a-radio-button>
      </a-radio-group>

      <a-tabs v-model:activeKey="activeKey" tab-position="left" :style="{ height: '500px' }">
        <!-- <a-tab-pane v-for="i in 30" :key="i" :tab="`Tab-${i}`">Content of tab {{ i }}</a-tab-pane> @tabScroll="callback"-->
        <a-tab-pane v-for="category in currentList.categories" 
                    :key="category.name" 
                    :tab="`Tab-${category.name}`">
           <p style="color: #888; margin-bottom: 12px;">{{ category.remark }}</p>

          <!-- 具体物品展示列表，试图复制可修改列表。 -->
          <a-table :columns="columns" 
                    :data-source="itemsByCategory[category.name]" 
                    :row-key="(record: FlatItem) => record.key"
                    :pagination="false">

            <template #bodyCell="{ column, record }">
              <!-- 物品名称列：编辑态 / 展示态 -->
              <template v-if="column.dataIndex === 'name'">
                <div v-if="editableData[record.key]">
                  <a-input v-model:value="editableData[record.key].name" />
                </div>
                <a v-else>{{ record.name }}</a>
              </template>

              <!-- 重要性列 -->
              <template v-else-if="column.dataIndex === 'importance'">
                <div v-if="editableData[record.key]">
                  <a-select v-model:value="editableData[record.key].importance">
                    <a-select-option value="important">重要</a-select-option>
                    <a-select-option value="unimportant">不重要</a-select-option>
                  </a-select>
                </div>
                <span v-else>{{ record.importance === 'important' ? '重要' : '不重要' }}</span>
              </template>

              <!-- 备注列 -->
              <template v-else-if="column.dataIndex === 'remark'">
                <div v-if="editableData[record.key]">
                  <a-input v-model:value="editableData[record.key].remark" />
                </div>
                <span v-else>{{ record.remark }}</span>
              </template>
              
              <!-- 是否已备齐？checkbox -->
              <template v-else-if="column.dataIndex === 'itemState'">
                <a-checkbox
                  :checked="record.itemState === 'yes'"
                  @change="(e: any) => toggleDone(record, e.target.checked)"
                />
              </template>

              <!-- 操作列 -->
              <template v-else-if="column.dataIndex === 'operation'">
                <div v-if="editableData[record.key]">
                  <a @click="save(record.key)">保存</a>
                  <a-divider type="vertical" />
                  <a @click="cancel(record.key)">取消</a>
                </div>
                <a v-else @click="edit(record.key)">编辑</a>
              </template>
            </template>
          </a-table>

        </a-tab-pane>
      </a-tabs>
    </div>

  </div>
</template>


<script lang="ts" setup>
import { ref, computed, UnwrapRef, reactive,watch } from 'vue';
import { cloneDeep } from 'lodash-es';
import type {  TableColumnType } from 'ant-design-vue';
import { Importance, isDone, type ShoppingList, type Item } from '../../../../types'
import { travelList, localList } from '../../../../types/data.ts'

// 切换视图显示========================================
// ✅ 用独立的变量控制"视图模式"，不要和 tab-position 混用
const viewMode = ref<'travel' | 'local'>('travel')
const activeKey = ref(travelList.categories[0].name)

// ✅ 根据 viewMode 切换数据源
const currentList = computed<ShoppingList>(() => {
  return viewMode.value === 'travel' ? travelList : localList
})

// ✅ 切换视图时：重置 activeKey + 清空未保存的编辑态
watch(viewMode, () => {
  activeKey.value = currentList.value.categories[0]?.name ?? ''
  Object.keys(editableData).forEach(k => delete editableData[k])
})
// 切换视图显示 END========================================

/** 判断是否重要（模板中用） */
const isImportant = (item: Item) => item.importance === Importance.Important


// 尝试覆写，改造物品展示列表==============================

// ====== 表格列配置 ======
interface FlatItem extends Item {
  categoryName: string;
}

// 扁平化为 FlatItem[]
// const flatItems = computed(() =>
//   currentList.value.categories.flatMap((category, catIdx) =>
//     category.items.map((item, itemIdx) => ({
//       ...item, // 复制 Item 的所有字段（包括 key）
//       key: `${catIdx}-${itemIdx}`,       // ✅ 唯一
//       categoryName: category.name // 追加类别名
//     }))
//   )
// );

// ====== 按类别分组的扁平化数据（核心修改）======
const itemsByCategory = computed(() => {
  const map: Record<string, FlatItem[]> = {}
  currentList.value.categories.forEach((category, catIdx) => {
    map[category.name] = category.items.map((item, itemIdx) => ({
      ...item,
      key: `${catIdx}-${itemIdx}`,   // 全局唯一 key（保留你之前的修复）
      categoryName: category.name,
    }))
  })
  return map
})

const columns: TableColumnType<FlatItem>[] = [
  { title: '物品名称', dataIndex: 'name', width: 150 },
  { title: '重要性', dataIndex: 'importance', width: 100 },
  { title: '备注', dataIndex: 'remark' },
  { title: '已备齐', dataIndex: 'itemState', width: 80 },
  { title: '操作', dataIndex: 'operation', width: 150 }  // 操作列
];

const editableData: UnwrapRef<Record<string, FlatItem>> = reactive({});

// 关于物品是否已备齐
const toggleDone = (record: FlatItem, checked: boolean) => {
  const [catIdx, itemIdx] = record.key.split('-').map(Number)
  currentList.value.categories[catIdx].items[itemIdx].itemState =
    checked ? isDone.Done : isDone.notDone
}

// 编辑行功能
const edit = (key: string) => {
  // editableData[key] = cloneDeep(flatItems.value.filter(item => key === item.key)[0]);
  const [catIdx, itemIdx] = key.split('-').map(Number)
  const category = currentList.value.categories[catIdx]
  const item = category?.items[itemIdx]

  if (item) {
    editableData[key] = cloneDeep({
      ...item,
      key,                        // 保留唯一 key
      categoryName: category.name // 保留类别名（编辑态可能用到）
    })
  }
};

const save = (key: string) => {
  // Object.assign(flatItems.value.filter(item => key === item.key)[0], editableData[key]);
  // delete editableData[key];
  
  // 这个改的只是复制的数据
  // const target = flatItems.value.find(item => item.key === key);
  // if (target) {
  //   Object.assign(target, editableData[key]);
  // }
  // delete editableData[key];

  // 尝试修改源数据
  const [catIdx, itemIdx] = key.split('-').map(Number)
  const sourceItem = currentList.value.categories[catIdx]?.items[itemIdx]
  if (sourceItem) {
    const { key: _k, categoryName: _c, ...editFields } = editableData[key]
    Object.assign(sourceItem, editFields)   // ✅ 真正写回 travelList / localList
  }
  delete editableData[key]
};

const cancel = (key: string) => {
  delete editableData[key];
};
</script>

<style scoped>
.editable-row-operations a {
  margin-right: 8px;
}
</style>
