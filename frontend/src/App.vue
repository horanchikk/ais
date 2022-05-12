<template>
  <div class="flex flex-col w-screen h-screen bg-gray-900">
    <Toast position="top-left" />
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
            :label="`Авторизирован под ${this.username}`"
            class="p-button-raised p-button-success p-button-text"
            @click="showState(1)"
          />
          <div v-else class="flex gap-3">
            <Button
              label="Войти на сайт"
              class="p-button-raised p-button-warning p-button-text"
              @click="showState(0)"
            />
          </div>
        </div>
      </div>
    </header>
    <div class="flex-auto bg-gray-900">
      <router-view />
    </div>
    <Dialog v-model:visible="displayState" :modal="true" :draggable="false">
      <template #header>
        <div class="flex flex-col">
          <h1 v-if="state == 0" class="text-xl">Войдите на сайт</h1>
          <h1 v-else-if="state == 1" class="text-xl">Выход из аккаунта</h1>
        </div>
      </template>

      <div class="col-5 flex justify-content-center">
        <div class="flex flex-col justify-center w-full" v-if="state == 0">
          <div class="flex flex-col justify-center">
            <label for="username">Имя пользователя </label>
            <InputText id="username" type="text" v-model="username" />
          </div>
          <br />
          <div class="p-fluid">
            <label for="password">Пароль</label>
            <Password v-model="password" />
          </div>
          <br />
          <br />
        </div>
        <div class="flex justify-center w-full" v-else-if="state == 1">
          <h1>Вы уверены, что хотите выйти?</h1>
        </div>
      </div>

      <template #footer>
        <div v-if="state == 0">
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
            @click="login('reg')"
          />
          <Button
            label="Войти"
            icon="pi pi-users"
            class="p-button-text"
            autofocus
            @click="login('login')"
          />
        </div>
        <div v-if="state == 1" class="w-full flex justify-center">
          <Button
            label="Нет"
            icon="pi pi-times"
            @click="displayState = false"
            class="p-button-text"
          />
          <Button
            label="Да"
            icon="pi pi-user-plus"
            class="p-button-text"
            @click="login('logout')"
            autofocus
          />
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script>
import Sidebar from "primevue/sidebar";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import CinemaAPI from "/src/mixins/cinemaApi.js";
import Password from "primevue/password";
import InputText from "primevue/inputtext";
import Toast from "primevue/toast";
import cinemaApi from "./mixins/cinemaApi";

export default {
  data() {
    return {
      state: 0,
      userid: null,
      username: null,
      password: null,
      errorText: null,
      displayState: false,
    };
  },
  components: {
    Button,
    Dialog,
    Password,
    InputText,
    Toast,
    Sidebar,
  },
  mixins: [CinemaAPI],
  methods: {
    showState(state) {
      this.displayState = true;
      this.state = state;
    },
    logout() {
      this.displayState = false;
      this.userid = null;
    },
    async login(mode) {
      if (mode == "login") {
        let req = await cinemaApi.login(this.username, this.password);

        if (req["status"] == 400) {
          if (req["detail"]["code"] == 1) {
            this.errorText = req["detail"]["message"];
            this.$toast.add({
              severity: "error",
              summary: this.errorText,
              life: 2000,
            });
            this.userid = null;
            this.errorText = null;
          }
        } else {
          this.userid = this.username;
          this.displayState = false;
          this.$toast.add({
            severity: "success",
            summary: "Вы были авторизованы!",
            life: 2000,
          });
        }
      } else if (mode == "reg") {
        await cinemaApi.reg(this.username, this.password);
        this.userid = this.username;
        this.displayState = false;
        this.$toast.add({
          severity: "success",
          summary: "Вы были зарегистрированы",
          life: 2000,
        });
      } else if (mode == "logout") {
        this.userid = null;
        this.displayState = false;
        this.$toast.add({
          severity: "success",
          summary: "Вы вышли из аккаунта",
          life: 2000,
        });
      }
    },
  },
};
</script>

<style />
