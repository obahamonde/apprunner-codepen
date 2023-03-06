<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";

const { state, notify } = useStore();
const { user } = useAuth0();

const getPencils = async () => {
  const { data } = await useFetch(`/api/code?sub=${user.value.sub!}`).json();
  state.pencils = unref(data) as any;
};

const deletePencil = async (key: string) => {
  await useFetch(`/api/code?key=${key}`, {
    method: "DELETE",
  });

  await getPencils();
};

onMounted(async () => {
  await getPencils();
});
</script>
<template>
  <section>
    <div grid3 p-8 gap-4>
      <div v-for="pencil in state.pencils" col>
        <VCard>
          <VCardTitle
            class="text-lg font-bold text-gray-700 dark:text-gray-200 bg-blue-100 dark:bg-gray-800 text-center row"
            >{{ pencil.title }}
            <Icon
              icon="mdi-delete"
              text-gray-700
              hover:text-red-700
              scale
              cp
              right-0
              absolute
              m-1
              @click="deletePencil(pencil.key!)"
              >mdi-delete</Icon
            ></VCardTitle
          >
          <iframe
            :src="pencil.url"
            class="w-full h-full sh"
            frameborder="0"
            scrolling="no"
            allowtransparency="true"
            allowfullscreen="true"
          ></iframe>
        </VCard>
      </div>
    </div>
  </section>
</template>
