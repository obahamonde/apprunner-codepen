<script setup lang="ts">
import { options } from "../hooks";
import MonacoEditor from "monaco-editor-vue3";
const isDark = ref(false);
const { state } = useStore();
</script>

<template>
  <div row h-screen>
    <MonacoEditor
      :theme="isDark ? 'vs-dark' : 'vs'"
      :options="options"
      language="html"
      v-model:value="state.code.code"
      class="h-1/2"
    />
    <iframe :srcdoc="state.code.code" class="w-full" />
  </div>
</template>
