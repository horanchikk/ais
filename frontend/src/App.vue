<template>
  <div class="flex flex-col w-screen h-screen bg-gray-900">
    <!-- Список билетов  -->
    <Sidebar v-model:visible="showTickets">
      <template #header>
        <h3>Список купленных билетов</h3>
      </template>
      <div class="h-full">
        <div
          v-for="film in userTickets"
          :key="film"
          class="flex flex-col justify-center items-center py-5"
        >
          <QrcodeVue
            :value="`${encode(
              'http://localhost:3000/#?checkticket=true&user=' +
                this.userid +
                '&film=' +
                film.id
            )}`"
            :size="300"
            :background="'#fff'"
            :foreground="'#000000'"
            :level="'L'"
          ></QrcodeVue>
          <h1>{{ film.name }}</h1>
        </div>
      </div>
    </Sidebar>

    <!-- Уведомления -->
    <Toast position="top-left" />

    <!-- Хедер  -->
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
              class="p-button-raised p-button-success"
              @click="showState(1)"
            />
            <Button
              :label="`Список билетов [${this.userTickets.length}]`"
              class="p-button-raised p-button-help"
              @click="showTickets = true"
            />
            <Button
              v-if="this.userType == 'admin'"
              :label="'Проверка билетов'"
              class="p-button-raised p-button-primary"
              @click="scanTickets('start')"
            />
          </div>
          <div v-else class="flex gap-3">
            <Button
              label="Войти на сайт"
              class="p-button-raised p-button-warning"
              @click="showState(0)"
            />
          </div>
        </div>
      </div>
    </header>
    <div class="flex-auto bg-gray-900">
      <router-view />
    </div>
    <Dialog
      v-model:visible="displayState"
      :modal="true"
      :draggable="false"
      :closable="false"
    >
      <template #header>
        <div class="flex flex-col w-full items-center">
          <h1 v-if="state == 0" class="text-xl">Войдите на сайт</h1>
          <h1 v-else-if="state == 1" class="text-xl">Выход из аккаунта</h1>
          <h1 v-else-if="state == 99" class="text-xl">Проверка билетов</h1>
        </div>
      </template>

      <div class="col-5 flex justify-content-center">
        <div
          class="flex flex-col justify-center w-full"
          v-if="state == 0"
          @keyup.enter="login('login', this.username, this.password)"
        >
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
        <div class="flex flex-col w-full" v-else-if="state == 99">
          <qrcode-stream
            @decode="onDecode"
            :track="paintOutline"
            @init="logErrors"
          ></qrcode-stream>
          <p>Decoded: {{ this.decoded }}</p>
        </div>
        <div class="flex flex-col w-full" v-else-if="state == 90">
          <p>Покупатель: {{ this.buyerName }}</p>
          <p>Фильм: {{ this.buyerFilm }}</p>
          <br />
          <p class="text-green-500 text-center">Билет валиден.</p>
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
            @click="login('reg', this.username, this.password)"
          />
          <Button
            label="Войти"
            icon="pi pi-users"
            class="p-button-text"
            autofocus
            @click="login('login', this.username, this.password)"
          />
        </div>
        <div v-else-if="state == 1" class="w-full flex justify-center">
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
        <div class="flex w-full justify-center" v-else-if="state == 99">
          <Button
            :label="'Закрыть'"
            icon="pi pi-times"
            @click="scanTickets('stop')"
          />
        </div>
        <div class="flex w-full justify-center" v-else-if="state == 90">
          <Button
            :label="'Закрыть'"
            icon="pi pi-times"
            @click="closeTicket()"
          />
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script>
// PrimeVue компоненты
import Sidebar from "primevue/sidebar";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import Password from "primevue/password";
import InputText from "primevue/inputtext";
import Toast from "primevue/toast";

// Миксин для работы с жанрами и API
import cinemaApi from "./mixins/cinemaApi";

// Сторонние библиотеки

import QrcodeVue from "qrcode.vue";
import { QrcodeStream } from "qrcode-reader-vue3";

import base64 from "base-64";
import Cookies from "js-cookie";

export default {
  data() {
    return {
      // Данные вошедшего пользователя
      userid: null,
      userType: null,
      userTickets: [],

      // Данные при авторизации/регистрации
      username: null,
      password: null,

      // Данные купившего билеты пользователя
      buyerName: "",
      buyerFilm: "",

      // Стэйты
      state: 0,
      showTickets: false,
      displayState: false,
      // Обработка ошибок
      errorText: null,
      // Отладка
      debugging: false,
      mobileUI: false,
      decoded: "",
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
    QrcodeStream,
  },
  mixins: [cinemaApi],
  methods: {
    encode(text) {
      return base64.encode(text);
    },
    /**
     * Отображение отладочного сообщения
     * @param {string} msg сообщение для отладки
     */
    debug(msg) {
      if (this.debugging == true) {
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
    async userGET() {
      let req = await cinemaApi.getUserById(this.$route.query.user);
      this.buyerName = await req["response"]["login"];
      return await req["response"]["login"];
    },
    async filmGET() {
      let req = await cinemaApi.getFilmById(this.$route.query.film);
      this.buyerFilm = await req["response"]["name"];
      return await req["response"]["name"];
    },
    /**
     * Выход из аккаунта.
     */
    logout() {
      this.displayState = false;
      this.userid = null;
    },
    logErrors(promise) {
      promise.catch(console.error);
    },
    async updTicketsList(usr, passwd) {
      let req = await cinemaApi.login(usr, passwd);
      this.userTickets = [];
      for (const i in req["response"]["tickets"]) {
        let res = await cinemaApi.getFilmById(req["response"]["tickets"][i]);
        let a = {
          name: `${res["response"]["name"]}`,
          id: `${res["response"]["id"]}`,
        };
        this.userTickets.push(a);
      }
    },
    async login(mode, usr, passwd) {
      let severity = "success";
      let summary = "";
      this.debug(`logging as ${usr}`);

      if (mode == "login") {
        let req = await cinemaApi.login(usr, passwd);
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
          this.updTicketsList(usr, passwd);
          this.debug("list updated");
          this.displayState = false;
          summary = "Вы были авторизованы!";

          if (!Cookies.get("login") && !Cookies.get("password")) {
            Cookies.set("login", usr, { expires: 1 });
            Cookies.set("password", passwd, { expires: 1 });
            this.debug(`Cookie set: ${usr}, ${passwd}`);
          } else {
            this.username = Cookies.get("login");
            this.password = Cookies.get("password");
          }
        }
      } else if (mode == "reg") {
        let req = await cinemaApi.reg(usr, passwd);
        if (req["status"] == 400 || req["status"] == 422) {
          this.userid = null;
          this.errorText = req["detail"]["message"];
          severity = "error";
          summary = this.errorText;
          if (summary == undefined) {
            summary = `Ошибка сервера. Обратитесь к разработчику. Ошибка: ${req["detail"][0]["msg"]}`;
          }
        } else {
          this.userid = req["response"]["id"];
          this.userType = req["response"]["role"];
          this.updTicketsList(usr, passwd);
          this.displayState = false;
          summary = "Вы были зарегистрированы";
        }
      } else if (mode == "logout") {
        this.userid = null;
        this.displayState = false;
        Cookies.remove("login");
        Cookies.remove("password");
        this.debug("cookies removed");
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
    paintOutline(detectedCodes, ctx) {
      for (const detectedCode of detectedCodes) {
        const [firstPoint, ...otherPoints] = detectedCode.cornerPoints;

        ctx.strokeStyle = "green";
        ctx.lineWidth = 10;
        ctx.fillStyle = "#111111";

        ctx.beginPath();
        ctx.moveTo(firstPoint.x, firstPoint.y);
        for (const { x, y } of otherPoints) {
          ctx.lineTo(x, y);
        }

        ctx.lineTo(firstPoint.x, firstPoint.y);

        ctx.closePath();
        ctx.stroke();
      }
    },
    async checkTicket() {
      // Меню кассира
      if (this.$route.query.checkticket == "true") {
        // если в запросе есть checkticket
        if (this.$root.$data.userType == "admin") {
          // и авторизированный пользовать == admin
          if (this.$route.query.user != "" && this.$route.query.film != "") {
            // то проверем запрос на наличие пустых строк
            this.state = 90;
            this.displayState = true;
            document.title = "Окно кассира";
            // вызываем окно для кассира
            await this.filmGET(this.$route.query.film);
            await this.userGET(this.$route.query.user);
            // берём данные пользователя. фильма и рендерим в окно
            this.debug("checkticket is working");
          }
        } else {
          this.$toast.add({
            severity: "error",
            summary: "У вас нет доступа к меню кассира.",
            life: 4500,
          });
          // если авторизированный пользователь не admin, то выводим данное сообщение
        }
      }
    },
    scanTickets(mode) {
      if (this.$root.$data.userType == "admin") {
        this.state == 99;
        if (mode == "stop") {
          this.displayState = false;
        } else if (mode == "start") {
          this.showState(99);
        }
      } else {
        this.$toast.add({
          severity: "error",
          summary: "У вас нет доступа к меню кассира.",
          life: 4500,
        });
      }
    },
    closeTicket() {
      window.close();
    },
    onDecode(decodedString) {
      window.open(base64.decode(decodedString), "checkTicket");
      this.scanTickets("stop");
    },
  },
  mounted() {
    if (Cookies.get("login") && Cookies.get("password")) {
      this.login("login", Cookies.get("login"), Cookies.get("password"));
      this.debug(`Logging as ${Cookies.get("login")} using cookie`);
    }
  },
  updated() {
    this.checkTicket();
  },
};
</script>

<style />
