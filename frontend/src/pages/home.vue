<template>
  <div class="h-full w-full text-white">
    <div class="overflow-scroll">
      <div v-for="film in films" :key="film">
        <div :class="this.blockui('filmblock')">
          <div class="h-full justify-center items-center">
            <img
              :src="
                film.image
                  ? film.image
                  : 'https://lv-cake.ru/imgtmp/430_506_w/data/no-photo.png'
              "
              :alt="film.image ? film.image : 'photo not found'"
              class="text-sm h-96 rounded-lg"
            />
          </div>
          <div class="flex flex-col justify-between gap-3 w-full">
            <div class="flex flex-col gap-2">
              <p class="text-4xl">{{ film.name }}</p>
              <div class="typeFilms">
                <div
                  v-for="genre in film.genres"
                  :key="genre"
                  :label="genre"
                  :class="`border-2 rounded-md mr-4 py-1 px-1 inline-block w-fit cursor-default ${this.detectGenre(
                    genre
                  )}`"
                >
                  {{ genre }}
                </div>
              </div>
            </div>
            <p :class="this.blockui('filmdesc') + ' cursor-default'">
              {{ film.description }}
            </p>
            <div class="flex flex-col">
              <div class="w-full flex justify-end pt-4 pb-2 text-2xl">
                <p>{{ film.price }} Р</p>
              </div>
              <Button
                v-if="this.$root.$data.userid != null"
                label="Купить билет"
                class="p-button-raised p-button-success w-full"
                @click="buyTicket(film.name, film.id)"
              />
              <Button
                v-else
                label="Войдите в аккаунт для покупки билета"
                class="p-button-raised p-button-secondary w-full"
                @click="callLogin"
              />
            </div>
          </div>
        </div>
      </div>
      <div class="w-full text-center text-gray-600 py-3">
        We stand with 💙💛
      </div>
    </div>

    <Dialog v-model:visible="displayBuy" :modal="true" :draggable="false">
      <template #header>
        <div class="flex flex-col" v-if="state == 1">
          <h1 class="text-xl">
            Покупка билета на фильм "{{ this.filmdata.name }}"
          </h1>
          <br />
        </div>
      </template>

      <div v-if="state == 1">
        <div class="flex flex-col">
          <label for="dateformat">Выберите дату</label>
          <Calendar
            id="dateformat"
            v-model="selectedDate"
            dateFormat="mm.dd.yy"
          />
        </div>
      </div>

      <div v-if="state == 2">
        <div class="flex justify-center">
          <QrcodeVue
            :value="
              encode(
                `http://localhost:3000/#?checkticket=true&user=${this.$root.$data.userid}&film=${this.filmdata.filmid}`
              )
            "
            :size="300"
            :background="'#fff'"
            :foreground="'#000'"
            :level="'L'"
          ></QrcodeVue>
        </div>
      </div>

      <template #footer>
        <div v-if="state == 1">
          <Button
            label="Отмена"
            icon="pi pi-times"
            @click="displayBuy = false"
            class="p-button-text"
          />
          <Button
            label="Купить билет"
            icon="pi pi-check"
            @click="showQr"
            class="p-button-text"
            autofocus
          />
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script>
// PrimeVue компоненты
import Button from "primevue/button";
import Calendar from "primevue/calendar";
import InputText from "primevue/inputtext";
import Dialog from "primevue/dialog";

// Миксины для работы с жанрами и API
import Genre from "../mixins/genre.js";
import CinemaAPI from "../mixins/cinemaApi.js";

// Сторонние библиотеки
import QrcodeVue from "qrcode.vue";
import base64 from "base-64";

export default {
  data() {
    return {
      displayBuy: false,
      filmName: "TestFilm",
      selectedDate: null,
      filmdata: null,
      state: 1,
      films: [],
    };
  },
  components: {
    Button,
    Calendar,
    InputText,
    Dialog,
    QrcodeVue,
  },
  mixins: [Genre, CinemaAPI],
  methods: {
    async debug(msg) {
      if (this.$root.$data.debugging == true) {
        this.$toast.add({
          severity: "info",
          summary: `debug: ${msg}`,
          life: 1500,
        });
      }
    },
    async updTicketsList() {
      let req = await CinemaAPI.login(
        this.$root.$data.username,
        this.$root.$data.password
      );
      this.debug(this.$root.$data.username);
      this.debug(this.$root.$data.password);
      this.$root.$data.userTickets = [];
      this.$root.$data.userTicketsName = [];
      for (const i in req["response"]["tickets"]) {
        let res = await CinemaAPI.getFilmById(req["response"]["tickets"][i]);
        this.$root.$data.userTickets.push(req["response"]["tickets"][i]);
        this.$root.$data.userTicketsName.push(res["response"]["name"]);
      }
    },
    async buyTicket(filmName, filmId) {
      this.filmdata = {
        name: filmName,
        filmid: filmId,
      };
      this.state = 1;
      this.displayBuy = true;
    },
    async showQr() {
      if (this.displayBuy) {
        const date = Date.parse(this.selectedDate);
        const req = await CinemaAPI.buyTicket(
          this.filmdata.filmid,
          this.$root.$data.userid,
          date
        );
        this.state = 2;
        this.$toast.add({
          severity: "success",
          summary: "Билет успешно куплен, QR-код сохранён в личном кабинете",
          life: 4500,
        });
        this.updTicketsList();
        this.debug(req["response"]);
      } else {
        this.displayBuy = true;
        // Фикс ре-рендера и уведомление об этом пользователя
        this.debug(
          `re-render fixed (this.displayBuy == ${this.displayBuy} ; this.state == ${this.state})`
        );
        this.showQr();
      }
    },
    blockui(value) {
      if (this.$root.$data.mobileUI) {
        if (value === "filmblock") {
          return "flex gap-5 p-4 mx-2 my-5 bg-gray-700 rounded-lg";
        } else if (value === "filmdesc") {
          return "text-xl";
        }
      } else {
        if (value === "filmblock") {
          return "flex gap-5 p-4 mx-16 my-5 bg-gray-700 rounded-lg";
        } else if (value === "filmdesc") {
          return "text-2xl";
        }
      }
    },
    async userGET() {
      return await CinemaAPI.getUserById(this.$route.query.user)["response"][
        "login"
      ];
    },
    async filmGET() {
      return await CinemaAPI.getFilmById(this.$route.query.film)["response"][
        "name"
      ];
    },
    callLogin() {
      this.$root.$data.displayState = true;
      this.$root.$data.state = 0;
    },
    encode(text) {
      return base64.encode(text);
    },
    async fetchFilms() {
      const req = await CinemaAPI.getAllFilms();
      req["response"].forEach((e) => {
        this.films.push(e);
      });
      this.debug(`Films count: ${this.films.length}`);
    },
  },
  beforeMount() {
    this.fetchFilms();
    window.innerWidth < 600 ? (this.mobileUI = true) : (this.mobileUI = false);
  },
};
</script>

<style>
.p-datepicker {
  background-color: rgb(39, 47, 59);
}

.p-datepicker-header {
  background-color: rgb(39, 47, 59);
}
</style>
