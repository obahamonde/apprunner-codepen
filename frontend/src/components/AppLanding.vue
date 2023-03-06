<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";
const { loginWithRedirect } = useAuth0();
const { notify } = useStore()
</script>

<template>
  <div h-screen w-screen bg-gradient-to-r from-gray-700 via-gray-900 to-black>
    <div
      class="my-32 mx-64 col center p-8 shadow-black shadow-lg bg-gray-500 rounded-lg"
    >
      <h1 class="text-cyan text-4xl font-sans m-4">Welcome to CodePencil</h1>
      <img src="/logo.png" class="x6 m-4 cp scale hover:animate-pulse" 
      @click="notify({message:'Welcome to CodePencil',status:'success'})"      
      />
      <h1 class="text-white text-2xl font-mono m-4">
        Press the button below to Continue
      </h1>
      <button class="m-4 btn-post" @click="loginWithRedirect()">
        Get Started
      </button>
    </div>
  </div>
</template>
