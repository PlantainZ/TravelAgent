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
        <a-tab-pane v-for="category in currentList.categories" :key="category.name" :tab="`Tab-${category.name}`">
          {{ category.remark }}

          <!-- 具体物品展示列表，试图复制可修改列表。 -->
          <a-table :columns="columns" :data-source="flatItems" :row-key="(record: FlatItem) => record.key">
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
                <span v-else>{{ record.importance }}</span>
              </template>

              <!-- 备注列 -->
              <template v-else-if="column.dataIndex === 'remark'">
                <div v-if="editableData[record.key]">
                  <a-input v-model:value="editableData[record.key].remark" />
                </div>
                <span v-else>{{ record.remark }}</span>
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
import { ref, computed, UnwrapRef, reactive } from 'vue';
import { cloneDeep } from 'lodash-es';
import type {  TableColumnType } from 'ant-design-vue';
import { Importance, isDone, type ShoppingList, type Item } from '../../types/index'
import { travelList, localList } from '../../types/data'

// 切换视图显示========================================
// ✅ 用独立的变量控制"视图模式"，不要和 tab-position 混用
const viewMode = ref<'travel' | 'local'>('travel')
const activeKey = ref('')

// ✅ 根据 viewMode 切换数据源
const currentList = computed<ShoppingList>(() => {
  return viewMode.value === 'travel' ? travelList : localList
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
const flatItems = computed(() =>
  currentList.value.categories.flatMap((category, catIdx) =>
    category.items.map((item, itemIdx) => ({
      ...item, // 复制 Item 的所有字段（包括 key）
      key: `${catIdx}-${itemIdx}`,       // ✅ 唯一
      categoryName: category.name // 追加类别名
    }))
  )
);

const columns: TableColumnType<FlatItem>[] = [
  { title: '类别', dataIndex: 'categoryName', width: 100 },
  { title: '物品名称', dataIndex: 'name', width: 150 },
  { title: '重要性', dataIndex: 'importance', width: 100 },
  { title: '备注', dataIndex: 'remark' },
  { title: '操作', dataIndex: 'operation', width: 150 }  // 操作列
];

const editableData: UnwrapRef<Record<string, FlatItem>> = reactive({});

const edit = (key: string) => {
  // editableData[key] = cloneDeep(flatItems.value.filter(item => key === item.key)[0]);
  const target = flatItems.value.find(item => item.key === key);  // ✅ find 而非 filter[0]
  if (target) {
    editableData[key] = cloneDeep(target);
  }
};

const save = (key: string) => {
  // Object.assign(flatItems.value.filter(item => key === item.key)[0], editableData[key]);
  // delete editableData[key];
  const target = flatItems.value.find(item => item.key === key);
  if (target) {
    Object.assign(target, editableData[key]);
  }
  delete editableData[key];
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
