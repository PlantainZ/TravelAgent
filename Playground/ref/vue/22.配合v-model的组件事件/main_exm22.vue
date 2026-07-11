<template>
    <h3>Main</h3>
    
    <p>搜索内容为：{{ search }}</p>
    <SearchComponent @searchEvent = "getSearch" />
</template>

<script>
import SearchComponent from './searchComponent.vue';
    export default {
        data(){
            return{
                search:""
            }
        },
        component:{
            searchComponent
        },
        method:{
            getSearch(data){
                this.search = data;
            }
        }
    }
</script>