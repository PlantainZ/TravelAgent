> import StyleDemo from "./components/StyleDemo.vue";

style的绑定

```vue
/*
style的绑定
*/

<!-- 仅限测试用，不推荐正式用！！！用css -->

<template>
    <p :style="p_style">Style绑定</p>
</template>

<script>
import {resolveDirective} from "vue";

export default {
    data() {
        return {
            p_style: {
                color: "green",
                fontSize: 40 + "px"
            }
        }
    },
    methods: {resolveDirective},
    computed: {}
}
</script>
```
