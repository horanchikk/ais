<template>
  <div class="flex flex-col w-screen h-screen bg-gray-900">
    <Sidebar v-model:visible="showTickets">
      <template #header>
        <h3>Список купленных билетов</h3>
      </template>
      <div class="h-full">
        <div
          v-for="film in userTicketsName"
          :key="film"
          class="flex flex-col justify-center items-center py-5"
        >
          <QrcodeVue
            :value="`http://localhost:3000/#?checkticket=true&user=${this.$root.$data.userid}&film=${film.id}`"
            :size="230"
            :background="'#1f1f1f'"
            :foreground="'#fff'"
          ></QrcodeVue>
          <h1>{{ film.name }}</h1>
        </div>
      </div>
    </Sidebar>
    <Toast position="top-left" />
    <header class="text-white bg-gray-600">
      <div class="flex justify-between w-screen">
        <div
          class="flex items-center px-4 font-extrabold text-3xl cursor-default"
        >
          <router-link to="/"> AIS </router-link>
        </div>
        <div class="flex p-3 gap-3">
          <div v-if="userid != null" class="flex gap-4">
            <Button
              :label="`Авторизирован под ${this.username}`"
              class="p-button-raised p-button-success p-button-text"
              @click="showState(1)"
            />
            <Button
              :label="`Список билетов [${this.userTickets.length}]`"
              class="p-button-raised p-button-help p-button-text"
              @click="showTickets = true"
            />
          </div>

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
            @keydown.enter="login('login')"
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
import QrcodeVue from "qrcode.vue";
import base64 from "base-64";

export default {
  data() {
    return {
      // horanchikk_test1 helloworld
      // Данные вошедшего пользователя
      userid: null,
      userType: null,
      userTickets: [],
      userTicketsName: [],
      // Данные при авторизации/регистрации
      username: null,
      password: null,
      // Стэйты
      state: 0,
      showTickets: false,
      displayState: false,
      // Обработка ошибок
      errorText: null,
      // Отладка
      debugging: false,
    };
  },
  components: {
    Button,
    Dialog,
    Password,
    InputText,
    Toast,
    Sidebar,
    QrcodeVue,
  },
  mixins: [CinemaAPI],
  methods: {
    encode(text) {
      console.log(`encoded: ${text}`);
      return base64.encode(text);
    },
    debug(msg) {
      if (this.$root.$data.debugging == true) {
        this.$toast.add({
          severity: "info",
          summary: `debug: ${msg}`,
          life: 1500,
        });
      }
    },
    showState(state) {
      this.displayState = true;
      this.state = state;
    },
    logout() {
      this.displayState = false;
      this.userid = null;
    },
    async updTicketsList() {
      let req = await CinemaAPI.login(
        this.$root.$data.username,
        this.$root.$data.password
      );
      this.$root.$data.userTickets = [];
      this.$root.$data.userTicketsName = [];
      for (const i in req["response"]["tickets"]) {
        let res = await CinemaAPI.getFilmById(req["response"]["tickets"][i]);
        this.$root.$data.userTickets.push(req["response"]["tickets"][i]);
        let a = {
          name: `${res["response"]["name"]}`,
          id: `${res["response"]["name"]}`,
        };
        this.$root.$data.userTicketsName.push(a);
      }
    },
    async login(mode) {
      let severity = "success";
      let summary = "";

      if (mode == "login") {
        let req = await cinemaApi.login(this.username, this.password);
        if (req["status"] == 400) {
          if (req["detail"]["code"] == 1) {
            this.userid = null;
            this.errorText = req["detail"]["message"];
            severity = "error";
            summary = this.errorText;
          }
        } else {
          this.userid = req["response"]["id"];
          this.userType = req["response"]["role"];
          this.updTicketsList();
          this.debug("list updated");
          this.displayState = false;
          summary = "Вы были авторизованы!";
        }
      } else if (mode == "reg") {
        let req = await cinemaApi.reg(this.username, this.password);
        if (req["status"] == 400) {
          this.userid = null;
          this.errorText = req["detail"]["message"];
          severity = "error";
          summary = this.errorText;
        } else {
          this.userid = req["response"]["id"];
          this.userType = req["response"][""];
          this.displayState = false;
          summary = "Вы были зарегистрированы";
        }
      } else if (mode == "logout") {
        this.userid = null;
        this.displayState = false;
        summary = "Вы вышли из аккаунта";
      }
      if (summary != "") {
        this.$toast.add({
          severity: severity,
          summary: summary,
          life: 2000,
        });
      }
    },
  },
};
</script>

<style />
