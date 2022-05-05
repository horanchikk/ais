<template>
  <div class="flex flex-col w-screen h-screen bg-gray-900">
    <header class="text-white bg-gray-600 flex justify-between">
      <div
        class="flex items-center px-4 font-extrabold text-3xl cursor-default"
      >
        <router-link to="/"> AIS </router-link>
      </div>
      <div class="flex p-3 gap-3">
        <Button
          v-if="userid != null"
          :label="`Авторизирован под ${this.userid}`"
          class="p-button-raised p-button-success p-button-text"
        />
        <div v-else class="flex gap-3">
          <Button
            label="Авторизация"
            class="p-button-raised p-button-warning p-button-text"
            @click="showState(true)"
          />
          <Button
            label="Регистрация"
            class="p-button-raised p-button-help p-button-text"
            @click="showState(false)"
          />
        </div>
        <!-- https://www.primefaces.org/primevue/splitbutton for adaptive -->
      </div>
    </header>
    <div class="flex-auto">
      <router-view />
    </div>
    <Dialog v-model:visible="displayState" :modal="true" :draggable="false">
      <template #header>
        <div class="flex flex-col">
          <h1 class="text-xl">
            {{ registrationState ? "Регистрация" : "Авторизация" }}
          </h1>
        </div>
      </template>

      <div class="confirmation-content">как сделать то</div>

      <template #footer>
        <!-- <Button
          label="Отмена"
          icon="pi pi-times"
          @click="displayState = false"
          class="p-button-text"
        />
        <Button
          label="Купить билет"
          icon="pi pi-check"
          @click="state = 2"
          class="p-button-text"
          autofocus
        /> -->
      </template>
    </Dialog>
  </div>
</template>

<script>
import Button from "primevue/button";
import Dialog from "primevue/dialog";

export default {
  data() {
    return {
      userid: null,
      registrationState: true,
      displayState: false,
    };
  },
  components: {
    Button,
    Dialog,
  },
  methods: {
    showState(state) {
      state
        ? (this.registrationState = false)
        : (this.registrationState = true);
      this.displayState = true;
    },
  },
};
</script>

<style />
