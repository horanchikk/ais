import { createRouter, createWebHashHistory } from "vue-router";
import notFound from "../pages/404.vue";
import home from "../pages/home.vue";
import schedule from "../pages/schedule.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: home,
  },
  {
    path: "/schedule",
    name: "schedule",
    component: schedule,
  },
  {
    path: "/:catchAll(.*)",
    name: "notFound",
    component: notFound,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
