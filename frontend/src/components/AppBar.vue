<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";
import { Code, Notify, User } from "../hooks";

const { state, notify } = useStore();

const { getAccessTokenSilently, user, logout } = useAuth0();

const title = computed(() => state.code.title);

const file = computed(
  () => new File([state.code.code], state.code.title, { type: "text/html" })
);

//Getting user info from the API
const getUserInfo = async () => {
  if (state.user) return;
  const token = await getAccessTokenSilently();
  const { data } = await useFetch(`/api/auth?token=${token}`).json();
  state.user = unref(data) as User;
  notify({
    message: `Welcome ${state.user.name}`,
    status: "success",
  });
};

const getPencils = async () => {
  const { data } = await useFetch(`/api/code?sub=${user.value.sub!}`).json();
  state.pencils = unref(data) as any;
};

const uploadFile = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);
  const { data } = await useFetch(
    `/api/upload?sub=${user.value.sub!}`,

    {
      method: "POST",
      body: formData,
    }
  ).text();
  const key = `/${user.value.sub!}/pencils/${state.code.title}.html`;
  const url = unref(data) as string;
  const code: Code = {
    title: state.code.title,
    description: state.code.description,
    tags: state.code.tags,
    url: url,
    key: key,
    created_at: new Date().toLocaleString(),
  };
  const { data: codeData } = await useFetch(
    `/api/code?sub=${user.value.sub!}`,
    {
      method: "POST",
      body: JSON.stringify(code),
    }
  ).json();

  const noti = JSON.parse(unref(codeData)) as Notify;
  notify({
    'message':"Pencil saved",
    'status':"success"
  })
  await getPencils();
};

onMounted(async () => {
  await getUserInfo();
});

const toggleTittle = ref(false);

const showMenu = ref(false);

const tag = ref("");

const dialog = ref(false);
</script>
<template>
  <div bg-primary row items-center py-2 px-4>
    <img
      src="/logo.png"
      class="invert x2 m-2 cp scale"
      @click="toggleTittle = !toggleTittle"
    />
    <div col start mx-2>
      <h1 class="text-title text-lg row start" v-if="!toggleTittle">
        {{ title }}
      </h1>
      <input
        type="text"
        v-model="state.code.title"
        v-if="toggleTittle"
        class="text-title text-lg row start"
        bg-primary
        @keyup.enter="toggleTittle = !toggleTittle"
      />
      <small class="text-muted text-xs text-caption row start">{{
        user.name
      }}</small>
    </div>
    <h1 mx-auto row center gap-4 text-white>
      <RouterLink to="/"
        title="Find Pencils"
        text-gray-700 hover:text-white
      ><Icon icon="mdi-home"  cp scale /></RouterLink>
      <RouterLink to="/about"
        title="Your Pencils"
        text-gray-700 hover:text-white
      ><Icon icon="mdi-information"  cp scale /></RouterLink>
      <RouterLink to="/editor"
        title="New Pencil"
        text-gray-700 hover:text-white
      ><Icon icon="mdi-pencil"  cp scale /></RouterLink>
    </h1>
    <div row center>
      <span
        class="row center text-caption cp scale right-60 bg-black px-4 rounded-lg sh absolute align-middle"
        @click="uploadFile(file)"
        ><Icon
          icon="mdi-cloud-upload-outline"
          class="x2 m-2 cp scale text-caption"
        />
        Save</span
      >
      <span
        class="row center text-caption cp scale right-20 bg-black px-4 rounded-lg sh absolute align-middle"
        @click="dialog = true"
        ><Icon
          icon="mdi-cog-outline"
          class="x2 m-2 cp scale text-caption text-xs"
        />
        Settings</span
      >
      <img
        :src="user.picture"
        class="x2 m-2 cp sh rf"
        @click="showMenu = !showMenu"
        right-4
        absolute
        align-middle
      />
      <div
        v-if="showMenu"
        class="absolute bg-success tr p-2"
        @click="showMenu = false"
      >
        <button class="btn-del mt-16" @click="logout()">Logout</button>
      </div>
    </div>
  </div>
  <VDialog
    v-model="dialog"
    title="Upload"
    width="500"
    height="500"
    :close-on-click-outside="false"
    :close-on-press-escape="false"
  >
    <div col center bg-black text-white rounded-lg sh p-4>
      <h1 text-body text-2xl>Pencil Info</h1>
      <label for="title" class="text-caption text-xs">Title</label>
      <input
        type="text"
        v-model="state.code.title"
        class="text-body p-2 m-2 rounded-lg text-xs w-75 row start"
        bg-primary
      />
      <label for="description" class="text-caption text-xs">Description</label>
      <textarea
        type="text"
        v-model="state.code.description"
        class="text-body p-2 m-2 rounded-lg text-xs row start w-75 h-full"
        bg-primary
      />
      <label for="tags" class="text-caption text-xs">Tags</label>
      <input
        type="text"
        v-model="tag"
        class="text-body p-2 m-2 rounded-lg text-xs row start w-75"
        bg-primary
        @keyup.enter="
          state.code.tags.push(tag);
          tag = '';
        "
      />
      <div grid-4 bg-gray-700 m-4 rounded-lg text-cyan w-75 h-full>
        <Icon
          v-if="state.code.tags.length"
          icon="mdi-delete-outline"
          class="x1 text-red-500 scale hover:text-red-700 m-2 cp scale text-caption text-xs tr"
          @click="state.code.tags = []"
        />
        <VChip
          v-for="tag in state.code.tags"
          :key="tag"
          class="m-2"
          color="red"
          closable
          clearable
        >
          {{ tag }}
        </VChip>
      </div>

      <div row center gap-4 p-4>
        <button
          cp
          scale
          px-4
          py-2
          bg-red-700
          text-white
          border-white
          hover:text-amber
          hover:border-amber
          rounded-lg
          sh
          w-32
          @click="dialog = false"
        >
          Cancel
        </button>
        <button
          cp
          scale
          px-4
          py-2
          bg-teal-700
          text-white
          border-white
          hover:text-amber
          hover:border-amber
          rounded-lg
          sh
          w-32
          @click="
            uploadFile(file);
            dialog = false;
          "
        >
          Save
        </button>
      </div>
    </div>
  </VDialog>
</template>
<style global>
.router-link-exact-active {
  @apply text-white;
}
</style>
