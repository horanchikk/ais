<template>
  <div class="flex flex-col w-screen h-screen bg-gray-900">
    <header class="text-white bg-gray-600">
      <div class="flex justify-between w-screen">
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
              label="Войти на сайт"
              class="p-button-raised p-button-warning p-button-text"
              @click="showState()"
            />
          </div>
          <!-- https://www.primefaces.org/primevue/splitbutton for adaptive (2k rubles) -->
        </div>
      </div>
    </header>
    <div class="flex-auto bg-gray-900">
      <router-view />
    </div>
    <Dialog v-model:visible="displayState" :modal="true" :draggable="false">
      <template #header>
        <div class="flex flex-col">
          <h1 class="text-xl">Войдите на сайт</h1>
        </div>
      </template>

      <div class="content-reg">
        <div class="col-5 flex align-items-center justify-content-center">
          <div class="flex flex-col justify-center align-center w-full">
            <div class="flex flex-col justify-center">
              <label for="username">Имя пользователя </label>
              <InputText id="username" type="text" v-model="userUsername" />
            </div>
            <br />
            <div class="p-fluid">
              <label for="password">Пароль</label>
              <Password v-model="userPassword" />
            </div>
            <br />
            <br />
          </div>
        </div>
      </div>

      <template #footer>
        <Button
          label="Отмена"
          icon="pi pi-times"
          @click="displayState = false"
          class="p-button-text"
        />
        <Button
          label="Зарегистрироваться"
          icon="pi pi-user-plus"
          class="p-button-text"
          autofocus
        />
        <Button
          label="Войти"
          icon="pi pi-users"
          class="p-button-text"
          autofocus
        />
      </template>
    </Dialog>
  </div>
</template>

<script>
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import CinemaAPI from "/src/mixins/cinemaApi.js";
import Password from "primevue/password";
import InputText from "primevue/inputtext";

export default {
  data() {
    return {
      userid: null,
      displayState: false,
    };
  },
  components: {
    Button,
    Dialog,
    Password,
    InputText,
  },
  mixins: [CinemaAPI],
  methods: {
    showState(state) {
      this.displayState = true;
    },
  },
};
</script>

<style />
