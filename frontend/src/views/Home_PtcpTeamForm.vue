<template>
  <a-list
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
        <template #actions>
          <a key="list-loadmore-edit">编辑</a>
          <a key="list-loadmore-more">更多</a>
        </template>

        <!-- 
        <a-skeleton> 是骨架屏组件，在数据未加载完成时显示占位动画。
         avatar：启用头像占位。
         :title="false"：不显示标题占位。
         :loading="!!item.loading"：是否显示骨架屏，取决于 item.loading 是否为真值。!! 是双重取反，用于把任意值转为布尔值（true/false）。
         active：骨架屏显示闪烁动画。
          -->
        <a-skeleton avatar :title="false" :loading="!!item.loading" active>
          <a-list-item-meta
            :description="item.signature"
          >
            <template #title>
              <a href="https://www.antdv.com/">{{ item.name.last }}</a> <!-- 后续可跳转用户界面 -->>
            </template>
            <template #avatar>
              <!-- <a-avatar :src="item.picture.large" /> -->
               <a-avatar :size="64" :src="item.profile" />
            </template>
          </a-list-item-meta>
          <div>正在修缮.....</div>
        </a-skeleton>
      </a-list-item>
    </template>
  </a-list>
</template>


<script lang="ts" setup>
import { onMounted, ref, nextTick } from 'vue';
const count = 4;
const fakeDataUrl = `https://randomuser.me/api/?results=${count}&inc=name,gender,email,nat,picture&noinfo`;

const fakeUserInfo = [{name:{last:'剑怜情'},signature:'Znn / 施工中....',profile:"/avatar/testProfile/剑怜情.jpg",email:'google.com'},
                      {name:{last:'玉镜川'},signature:'无敌是多么寂寞',profile:'/avatar/testProfile/玉镜川.jpg',email:'google.com'},
                      {name:{last:'卷积神经网络'},signature:'金风玉露一相逢',profile:'/avatar/testProfile/CNN.jpg',email:'google.com'},
                      {name:{last:'渡重绝'},signature:'便胜却人间无数',profile:'/avatar/testProfile/渡重绝.jpg',email:'google.com'}]

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
.demo-loadmore-list {
  min-height: 350px;
}
</style>
