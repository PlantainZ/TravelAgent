<template>
    <h3>祖宗</h3>
    <Parent/>
</template>

<script>
    import Parent from "./Parent.vue"

    export default {

        // provide:{
        //     message:"爷爷的财产"
        // },


        data(){
            return{
                msg:"爷爷的财产"
            }
        },
        provide(){ // 依赖注入，只能从上到下传。逆行全责！
            return{
                message:this.msg
            }
        },
        components:{
            Parent
        }
</script>