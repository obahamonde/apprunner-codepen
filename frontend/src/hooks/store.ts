import { defineStore, acceptHMRUpdate } from "pinia";
import { Notify, User, Code } from "./types";

export const useStore = defineStore("state", () => {
  const state = reactive({
    notifications: [] as Notify[],
    code: {
      id: "",
      code: `
      <h1></h1>
      <script>
        const el = document.querySelector("h1")
        el.innerText = "Hello World!"
      </script>
      <style>
        h1 {
          font-family: Merienda, cursive;
          color: #008080;
        }
      </style>`,
      title: "CodePencil",
      description: "",
      language: "html",
      tags: [] as string[],
    },
    pencils: [] as Code[],
    feed: [] as Code[],
    user: null as User | null,
  });

  const setState = (newState: any) => {
    Object.assign(state, newState);
  };

  const notify = (noti: Notify) => {
    state.notifications.push(noti);
    const audio = new Audio(`/audio/${noti.status}.mp3`);
    audio.play();
    setTimeout(() => {
      state.notifications.pop();
    }, 5000);
  };

  return {
    state,
    notify,
    setState,
  };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useStore, import.meta.hot));
}
