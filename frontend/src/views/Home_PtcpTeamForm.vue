<template>
  <a-list
    :grid="{ gutter:0, column: 4 }"

    
    class="demo-loadmore-list"
    :loading="initLoading"
    item-layout="horizontal"
    :data-source="list"
  >

    <template #loadMore>
      <div
        v-if="!initLoading && !loading"
        :style="{ textAlign: 'center', marginTop: '12px', height: '32px', lineHeight: '32px' }"
      >
        <!--暂时隐藏一下按钮-->
        <!-- <a-button @click="onLoadMore">loading more</a-button> -->
      </div>
    </template>

      

    <template #renderItem="{ item }"> <!-- 一个具名插槽 -->

      <a-list-item>
        <a-card
          class="user-card"
          hoverable
          :bodyStyle="{ 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            padding: '16px 8px',
            height: '100%' 
          }"
          :style="{ minHeight: '150px' }"
        >
          <a-skeleton avatar :title="false" :loading="!!item.loading" active>
            <div style="display: flex; flex-direction: column; align-items: center; gap: 12px; width: 100%;">

              <!-- 头像：不可压缩 -->
              <a-avatar :size="64" :src="item.profile" style="flex-shrink: 0;" />

              <!-- ✅ 修改点2：用户名单行完整显示，超出横向滚动 -->
              <a
                href="https://www.antdv.com/"
                class="user-name"
                :title="item.name.last" 
              >
                {{ item.name.last }}
              </a>

            </div>
          </a-skeleton>
        </a-card>
      </a-list-item>


    </template>
  </a-list>
</template>


<script lang="ts" setup>
import { onMounted, ref, nextTick } from 'vue';
const count = 4;
const fakeDataUrl = `https://randomuser.me/api/?results=${count}&inc=name,gender,email,nat,picture&noinfo`;

const fakeUserInfo = [{name:{last:'吟游诗人小卷'},signature:'平等地言语攻击所有人',profile:"/avatar/ptcpTeam/吟游诗人小卷.jpg",email:'google.com'},
                      {name:{last:'残差网络'},signature:'人类的伪捷径',profile:'/avatar/ptcpTeam/残差网络.jpg',email:'google.com'},
                      {name:{last:'纵时驰'},signature:'踏星行好了没',profile:'/avatar/ptcpTeam/纵时驰.jpg',email:'google.com'},
                      {name:{last:'龙角散'},signature:'吃起来很清凉',profile:'/avatar/ptcpTeam/龙角散.jpg',email:'google.com'},

                      {name:{last:'六边形稻草人'},signature:'恨明月高悬不独照我',profile:'/avatar/ptcpTeam/六边形稻草人.jpg',email:'google.com'},
                      {name:{last:'枇杷树下弹琵琶'},signature:'枇杷可不像牛一样不解风情',profile:'/avatar/ptcpTeam/枇杷树下弹琵琶.jpg',email:'google.com'},
                      {name:{last:'林芝地里挖灵芝'},signature:'骑猪打地洞',profile:'/avatar/ptcpTeam/林芝地里挖灵芝.jpg',email:'google.com'}]

const initLoading = ref(true);
const loading = ref(false);
const data = ref<any[]>([]);
const list = ref<any[]>([]);
onMounted(() => {
  // fetch(fakeDataUrl)
  //   .then(res => res.json()) // then是一种强制等待的行为！
  //   .then(res => {
  //     initLoading.value = false;
  //     data.value = res.results;
  //     list.value = res.results;
  //     console.log("取到的第一批用户list格式：",res.results);
  //   });
  initLoading.value = false;
  console.log('fakeUserInfo样子：',fakeUserInfo)
  data.value = fakeUserInfo;
  list.value = fakeUserInfo;

});

const onLoadMore = () => {
  loading.value = true;
  list.value = data.value.concat(
    [...new Array(count)].map(() => ({ loading: true, name: {}, picture: {} })),
  );
  fetch(fakeDataUrl)
    .then(res => res.json())
    .then(res => {
      const newData = data.value.concat(res.results);
      loading.value = false;
      data.value = newData;
      list.value = newData;
      nextTick(() => {
        // Resetting window's offsetTop so as to display react-virtualized demo underfloor.
        // In real scene, you can using public method of react-virtualized:
        // https://stackoverflow.com/questions/46700726/how-to-use-public-method-updateposition-of-react-virtualized
        window.dispatchEvent(new Event('resize'));
      });
    });
};
</script>

<style scoped>

.demo-loadmore-list:deep(.ant-list-item) {
  min-height: 150px;

  /*
  * deep()是样式穿透的意思。无视ant的限制。 
   * padding: 8px 意味着每个格子四周都有 8px 的空白。
   * 两张卡片相邻时，间距就是 8px + 8px = 16px。
   * 如果想让间距变成 6px，就把这里改成 padding: 3px !important;
   * !important是覆盖任何其它样式声明
   */
  padding: 8px !important; 
  
  /* 清除 Antd 默认的底部 margin，防止上下间距比左右宽 */
  margin-bottom: 0 !important; 
}



/* jlq_add */

.user-card {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  cursor: pointer;
  border-radius: 8px;
}

.user-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

/* ✅ 核心：单行完整显示，不换行，不截断 */
.user-name {
  font-size: 15px;
  font-weight: 500;
  text-align: center;
  display: block;
  width: 100%;
  box-sizing: border-box;
  
  /* 强制在一行，不换行 */
  white-space: nowrap;       
  flex-shrink: 0;            
  line-height: 1.4;
  
  /* ✅ 关键：不截断（去掉 ellipsis），允许溢出时横向滚动 */
  overflow-x: auto;
  overflow-y: hidden;
  
  /* 美化滚动条（使其尽可能不占高度、隐形） */
  scrollbar-width: thin; /* Firefox */
  scrollbar-color: transparent transparent; /* 默认隐藏，滚动时显示 */
}

/* Chrome/Safari 滚动条美化 */
.user-name::-webkit-scrollbar {
  height: 4px;
}
.user-name::-webkit-scrollbar-thumb {
  background: rgba(0,0,0,0.2);
  border-radius: 2px;
}
.user-name:hover::-webkit-scrollbar-thumb {
  background: rgba(0,0,0,0.4);
}

</style>
