```<!--
    每个绑定仅支持一个合法的语法
-->
<!--
    双花括号会将数据插值转换为纯文本，而不是html
    如果想插入html，那么需要使用v-html标签
-->
<template>
    <h3>模板语法</h3>
    <p>{{ msg }}</p>
    <p>{{ hello }}</p>
    <p>{{ number + 1 }}</p>
    <p>{{ ok ? "yes" : "No"}}</p>
    <p>{{message.split(" ").reverse().join(" ")}}</p>

    <!--错误语句：<p>{{var a=1}}</p>-->
    <p>{{ exampleHtml }}</p>  <!--这种操作并不会渲染html语法-->
    <p v-html="exampleHtml"></p>  <!--v-html是一种指令-->
</template>
<script>
// 文本插值语法
export default {
    data() {
        return {
            msg: "神奇的语法",
            hello: "hello world",
            number: 10,
            ok:true,
            message:"a b c d e f g",
            exampleHtml:"<a href='http://baidu.com'>ping一下百度</a>"
        }
    }
}
</script>
```