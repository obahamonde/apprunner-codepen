<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";
const { isAuthenticated, loginWithRedirect } = useAuth0();
</script>
<template>
  <div v-if="isAuthenticated">
    <RouterView />
    <AppNotifier />
  </div>
  <div v-else col center>
    <AppLanding />
  </div>
</template>
<style global>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
</style>
