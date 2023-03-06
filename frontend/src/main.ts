//main.ts
import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import { createPinia } from "pinia";
import App from "./App.vue";
import "uno.css";
import { Icon } from "@iconify/vue";
import generatedRoutes from "virtual:generated-pages";
import { setupLayouts } from "virtual:generated-layouts";
import { createAuth0 } from "@auth0/auth0-vue";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import "@mdi/font/css/materialdesignicons.css";

const routes = setupLayouts(generatedRoutes);

createApp(App)
  .use(
    createRouter({
      history: createWebHistory(import.meta.env.BASE_URL),
      routes,
    })
  )
  .use(
    createAuth0({
      domain: "dev-tvhqmk7a.us.auth0.com",
      clientId: "53p0EBRRWxSYA3mSywbxhEeIlIexYWbs",
      authorizationParams: {
        redirect_uri: window.location.origin,
      },
    })
  )
  .use(
    createVuetify({
      components,
      directives,
    })
  )
  .use(createPinia())
  .component("Icon", Icon)
  .mount("#app");
