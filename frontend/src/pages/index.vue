<script setup lang="ts">
import { Code } from "../hooks";

const { state } = useStore();


const fetchFeed = async()=>{
    const { data } = await useFetch("/api/feed").json();
    state.feed = unref(data) as Code[]
}

onMounted(async()=>{
    await fetchFeed()
})

</script>
<template>
<h1 text-title m-4  >All the Pencils</h1>
<section grid3 gap-8 p-8>
<VCard v-for="item in state.feed">
   <h1 px-2 py-1 bg-gray-300 row center><div col center mx-4><img :src="item.user.picture" class="x2 rf" />
    <small text-caption text-xs>{{item.user.name.split(" ")[0]}}</small>
    </div>
    <h1 class="text-body col center mx-4">{{item.title}}</h1>
    <p text-caption text-xs col center mx-4> {{ new Date(item.updated_at).toLocaleString() }}</p>
</h1>
    
    
    <iframe :src="item.url" style="width:100%;height:100%;"></iframe>
    
    <p>{{item.key}}</p>
</VCard>
</section>
</template>