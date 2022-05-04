<template>
  <div class="flex flex-col w-screen h-screen bg-gray-900">
    <header class="text-white bg-gray-600 flex justify-between">
      <div
        class="flex items-center px-4 font-extrabold text-3xl cursor-default"
      >
        <router-link to="/"> AIS </router-link>
      </div>
      <div class="flex p-5 gap-3">
        <!-- <router-link to="/schedule"
          ><Button
            label="Расписание"
            class="p-button-raised p-button-warning p-button-text"
        /></router-link> -->
        <!-- https://www.primefaces.org/primevue/splitbutton for adaptive -->
      </div>
    </header>
    <div class="flex-auto">
      <router-view />
    </div>
  </div>
</template>

<script>
import Button from "primevue/button";

export default {
  components: {
    Button,
  },
};
</script>

<style />
