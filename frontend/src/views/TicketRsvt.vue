<template>
    <a-tabs v-model:activeKey="activeKey" type="editable-card"
        @edit="onEdit" style="font-size:18px"><!-- <div > <div v-else> -->
        <a-tab-pane v-for="pane in panes" :key="pane.key" :tab="pane.title" :closable="pane.closable" >

            <div>
                <!-- 标题栏 div -->
                <div v-if="pane.isGrabbing" class="ticket-header" >
                    <span class="ticket-title-grabbing">{{ pane.title }}</span>
                    <span class="ticket-approach"> 公众号预约 </span>
                    <span class="ticket-time"> 2026.0725 </span>
                
                </div> 
                

                <div class="ticket-body">
                    <!-- 标签设置 -->
                    <div class="divider"></div>
                        <a-space :size="[0, 'large']" wrap >
                            <a-tag :bordered="false" color="processing" class="infoTag">正在预约...</a-tag>
                            <a-tag :bordered="false" color="success">success</a-tag>
                            <a-tag :bordered="false" color="error">error</a-tag>
                            <a-tag :bordered="false" color="warning">warning</a-tag>
                            <a-tag :bordered="false" color="magenta">magenta</a-tag>
                            <a-tag :bordered="false" color="red">red</a-tag>
                            <a-tag :bordered="false" color="volcano">volcano</a-tag>
                            <a-tag :bordered="false" color="orange">orange</a-tag>
                            <a-tag :bordered="false" color="gold">gold</a-tag>
                            <a-tag :bordered="false" color="lime">lime</a-tag>
                            <a-tag :bordered="false" color="green">green</a-tag>
                            <a-tag :bordered="false" color="cyan">cyan</a-tag>
                            <a-tag :bordered="false" color="blue">blue</a-tag>
                            <a-tag :bordered="false" color="geekblue">geekblue</a-tag>
                            <a-tag :bordered="false" color="purple">purple</a-tag>
                        </a-space>
                        <br/> <br/>



                <!-- 这是内容描述列表 -->
                <a-descriptions layout="vertical" bordered><!--去除 title="User Info"-->
                    <a-descriptions-item label="预约公众号" :span="3">
                        <div class="qrcode-cell">
                            <span class="qrcode-name">{{pane.title}}</span>

                            <!-- 增加显示二维码的气泡 -->
                            <a-popover v-model:open="visible" title="Title" trigger="click">
                                <template #content>
                                    <a-qrcode
                                        error-level="H"
                                        value="https://www.antdv.com"
                                        icon="https://www.antdv.com/assets/logo.1ef800a8.svg"
                                    />
                                    <a @click="hide">Close</a>
                                </template>
                                <a-button>点击我扫公众号二维码</a-button>
                            </a-popover>
                        </div>

                    </a-descriptions-item>
                    <a-descriptions-item label="票面选择日期" :span="3">2026.05.03</a-descriptions-item>
                    <a-descriptions-item label="票面选择时间" :span="3" >17：30</a-descriptions-item>
                    <a-descriptions-item label="票面选择信息" :span="3">一等座</a-descriptions-item>
                    <a-descriptions-item label="抢票开始时间" :span="1">2018-04-24 18:00:00</a-descriptions-item>
                    <a-descriptions-item label="Status" :span="1" >
                    <a-badge status="processing" text="Running" />
                    </a-descriptions-item>

                    <a-descriptions-item label="票价">20.00</a-descriptions-item>
                    <a-descriptions-item label="Official Receipts">$60.00</a-descriptions-item>
                    <a-descriptions-item label="注意事项">
                    {{ pane.content }}
                    </a-descriptions-item>
                </a-descriptions>

                <br/><br/><br/>
                <h3> 请认真阅读下方附加信息。 </h3>
                <!-- 补救措施的折叠面板 -->
                <a-collapse v-model:activeKey="activeKeyCollapse">
                <a-collapse-panel key="1" header="如果你抢不到票">
                <p>{{ text }}</p>
                </a-collapse-panel>
                <a-collapse-panel key="2" header="This is panel header 2">
                <p>{{ text }}</p>
                </a-collapse-panel>
                <a-collapse-panel key="3" header="This is panel header 3" collapsible="disabled">
                <p>{{ text }}</p>
                </a-collapse-panel>
            </a-collapse>

                </div><!-- 这是ticket-body的结束，为了限制整体的宽度。 -->

            </div>

        </a-tab-pane>
    </a-tabs>
</template>
<script lang="ts" setup>
import { ref,watch } from 'vue';


const panes = ref<{
    title: string;
    subTitle: string;
    isGrabbing: boolean;
    content: string;
    key: string;
    closable?: boolean
}[]>([
    {
        title: '泉州木偶剧院',
        subTitle: '抢票规则十分猎奇',
        isGrabbing: true,
        content: '提前写好观影人信息，抢票时会更迅速',
        key: '1'
    },
    {
        title: '闽台缘博物馆',
        subTitle: '泉州地标性建筑了算是',
        isGrabbing: false,
        content: 'Content of Tab 2', key: '2'
    },
    {
        title: '泉州非遗馆',
        subTitle: '外表破破烂烂的，经费全用到内装上了',
        isGrabbing: false,
        content: 'Content of Tab 3',
        key: '3',
        closable: false
    },
]);

const activeKey = ref(panes.value[0].key);

const newTabIndex = ref(0);

const add = () => {
    activeKey.value = `newTab${++newTabIndex.value}`;
    panes.value.push({
        title: '泉州木偶剧院',
        subTitle: '抢票规则十分猎奇',
        isGrabbing: true,
        content: 'Content of Tab 1，wowowowowo',
        key: '1'
    });
};

const remove = (targetKey: string) => {
    let lastIndex = 0;
    panes.value.forEach((pane, i) => {
        if (pane.key === targetKey) {
            lastIndex = i - 1;
        }
    });
    panes.value = panes.value.filter(pane => pane.key !== targetKey);
    if (panes.value.length && activeKey.value === targetKey) {
        if (lastIndex >= 0) {
            activeKey.value = panes.value[lastIndex].key;
        } else {
            activeKey.value = panes.value[0].key;
        }
    }
};

const onEdit = (targetKey: string | MouseEvent, action: string) => {
    if (action === 'add') {
        add();
    } else {
        remove(targetKey as string);
    }
};

//以下是折叠面板的变量
const text = `A dog is a type of domesticated animal.Known for its loyalty and faithfulness,it can be found as a welcome guest in many households across the world.`;
const activeKeyCollapse = ref(['1']);

watch(activeKeyCollapse, val => {
  console.log(val);
});

// 显示二维码的气泡组件
const visible = ref<boolean>(false);

const hide = () => {
  visible.value = false;
};

</script>

<style>
.ticket-header{
      display: flex;
    align-items: center;
    gap: 20px;
    justify-content: center; 
}

.TagShow{
      display: flex;
    align-items: center;
    gap: 20px;
    justify-content: center; 
}

.infoTag {
  padding-bottom: 5px;
  font-size: 14px;
  padding: 4px 12px;
}

/* 约束表格的整体宽度 */
.ticket-body {
    max-width: 990px;   /* 想要的宽度 */
    margin: 0 auto; /* 水平居中 */
}

.ticket-title-grabbing{
    /* 分别设置 左上、右上、左下、右下 四个方向的阴影 */
  /* text-shadow:
    5px 5px 0 rgb(101, 32, 32),
    -1px -1px 0 rgb(101, 32, 32),
    1px -1px 0 rgb(101, 32, 32),
    -1px 1px 0 rgb(101, 32, 32); */


  font-size: 49px;
  font-weight: 600;
  color: #491111;
  letter-spacing: 0.5px;
  line-height: 1.4;

}


.ticket-approach{
    font-size: 19px;
  font-weight: 600;
  color: #735e5e;
  letter-spacing: 0.5px;
  line-height: 1.4;
}

.ticket-time{}

/* 显示二维码的按钮*/
.qrcode-cell {
    display: flex;
    align-items: center;  /* 文字和按钮垂直居中对齐 */
    gap: 20px;            /* ← 精确的 20px 间距 */
}


/* 6. 深灰色横线 */
.divider {
  width: 100%;
  height: 1px;
  background-color: #b8b8b8;
  margin-top: 16px;
  margin-bottom: 12px;
}
</style>