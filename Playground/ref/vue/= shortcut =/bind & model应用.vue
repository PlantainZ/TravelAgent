<template>
  <div class="demo-container">
    <h2>v-bind 单向绑定示例</h2>
    <!-- 1. 使用 : 简写绑定图片的 src 属性 -->
    <img :src="avatarUrl" alt="Vue Logo" width="50" />
    
    <!-- 2. 使用 : 简写绑定按钮的 disabled 属性 -->
    <button :disabled="isButtonDisabled">
      提交 (当前状态: {{ isButtonDisabled ? '禁用' : '可用' }})
    </button>

    <h2>v-model 双向绑定示例</h2>
    <!-- 3. 使用 v-model 双向绑定输入框的值 -->
    <!-- 同时使用 @input 监听输入事件，动态改变按钮的状态 -->
    <input 
      v-model="username" 
      @input="checkInput" 
      placeholder="请输入用户名以启用按钮" 
    />
    
    <!-- 实时显示 username 的变化 -->
    <p>你好，{{ username }}！</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 用于 v-bind 的响应式数据
const avatarUrl = ref('https://vuejs.org/images/logo.png');
const isButtonDisabled = ref(true); // 初始状态为禁用

// 用于 v-model 的响应式数据
const username = ref('');

// 当输入内容不为空时，启用按钮
const checkInput = () => { // 关注数据流动：
                                // username容载了input框的输入变化。
                                // isButtonDisabled 仅接收改变讯号。
  isButtonDisabled.value = username.value.length === 0;
  // 注意这里，正则表达式的?前方，虽然是一个表达式或者是变量，但其实可以看作是一种bool变量。
};
</script>