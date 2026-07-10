> Path : ./myvue/src/components/ListDemo.vue


# 列表渲染

列表渲染

v-for="(item,index) in lists"

字典渲染

v-for="(value,key,index) in dicts"

# code

```vue
<template>
    <h1>列表渲染</h1>
    <div></div>
    <div>
        <p v-for="name in names">{{ name }}</p>
    </div>

    <div>
        <p v-for="some in dict">
            {{ some.id }},{{ some.name }}
            <!-- 此处使用属性绑定 -->
            <img :src="some.address" alt="">
        </p>
    </div>

    <div>
        <!-- (ex,index)=(元素和下标) -->
        <p v-for="(ex,index) in exs">
            {{ ex.name }} 's city is {{ ex.city }} : {{ index }}
        </p>
    </div>

    <!-- 遍历字典 -->
    <div>
        <p v-for="(value,key,index) in mydict">
            {{ value }} : {{ key }} : {{ index }}
        </p>
    </div>
</template>

<script>
export default {
    data() {
        return {
            names: ["aom", "som", "dom"],
            dict: [
                {
                    "id": 1001,
                    "name": "jom",
                    "address": "https://vcg00.cfp.cn/creative/vcg/800/new/VCG211401211159.jpg",
                },
                {
                    "id": 1002,
                    "name": "kom",
                    "address": "https://vcg00.cfp.cn/creative/vcg/800/new/VCG211401211159.jpg",
                },
                {
                    "id": 1003,
                    "name": "lom",
                    "address": "https://vcg00.cfp.cn/creative/vcg/800/new/VCG211401211159.jpg",
                },
            ],
            exs: [
                {"name": "qom", "city": "北京"},
                {"name": "wom", "city": "上海"},
                {"name": "eom", "city": "西安"},
            ],
            mydict: {
                "name": "com",
                "age": 19,
            }
        }
    }
}
</script>
```

