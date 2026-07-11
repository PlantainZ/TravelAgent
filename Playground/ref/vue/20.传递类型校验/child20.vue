<template>
    <h3>Chile</h3>
    <p>{{ checkType }}</p>
    <p>{{ age }}</p>

</template>

<script>
    export default {
        data(){
            return{}
        },
        props:{ // 注意，传过来的值都是只读的，不能通过method修改！
            checkType:{
                type:[String,Array,Object,Number], //不可以传函数哦

                required:true // 必选项，parent必须要传值过来！

            },// 数据来自parent，要用这四种方式存在！！
            // 如果不是这四种类型，console会warning

            age:{
                type:Number,
                default:20
            }, //即便没有传值过来，也会出现。
                //只能是String & number 类型有这种default!
            
                name:{
                type:Array,
                default(){
                    return ['空值']
                }//数组的默认返回方式比较特殊，要return！
            }
        },
        
        method:{
            updateHandle(){
                // 这是错误操作，props传来的数据是只读的！
                this.checkType = "修改数据"
            }
        }
    }

</script>