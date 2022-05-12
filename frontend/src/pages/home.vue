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
          <div class="flex flex-col justify-between gap-3 w-3/4">
            <div class="flex flex-col gap-2">
              <p class="text-4xl">{{ film.name }}</p>
              <div class="typeFilms">
                <div
                  v-for="genre in film.genres"
                  :key="genre"
                  :label="genre"
                  :class="`border-2 rounded-md mr-4 py-1 px-1 inline w-fit cursor-default ${this.detectGenre(
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
            <Button
              v-if="this.$root.$data.userid != null"
              label="Купить билет"
              class="p-button-raised p-button-success"
              @click="buyTicket(film.name, film.id)"
            />
            <Button
              v-else
              label="Войдите в аккаунт для покупки билета"
              class="p-button-raised p-button-secondary"
              @click="callLogin"
            />
          </div>
        </div>
      </div>
      <div class="w-full text-center text-gray-600">
        <h1>Всегда рады помощи :3</h1>
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
        <div v-if="state == 2">
          Билет успешно куплен, QR-код сохранён в личном кабинете.
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
                `http://localhost:3000/#?checkticket=true&user=2&film=${this.filmdata.filmid}`
              )
            "
            :size="300"
            :background="'#1f1f1f'"
            :foreground="'#fff'"
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
import Button from "primevue/button";
import Calendar from "primevue/calendar";
import InputText from "primevue/inputtext";
import Dialog from "primevue/dialog";
import Genre from "../mixins/genre.js";
import CinemaAPI from "../mixins/cinemaApi.js";
import QrcodeVue from "qrcode.vue";
import base64 from "base-64";

export default {
  data() {
    return {
      displayBuy: false,
      filmName: "TestFilm",
      selectedDate: null,
      mobileUI: false,
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
    async buyTicket(filmName, filmId) {
      this.filmdata = {
        name: filmName,
        filmid: filmId,
      };
      this.state = 1;
      this.displayBuy = true;
    },
    async showQr() {
      this.state = 2;
      if (this.displayBuy && this.state == 2) {
        const date = Date.parse(this.selectedDate);
        console.log(date);
        const req = await CinemaAPI.buyTicket(
          this.filmdata["filmid"],
          this.$root.$data.userid,
          date
        );
        console.log(req["response"]);
      }
    },
    blockui(value) {
      if (this.mobileUI) {
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
      console.log(this.films);
    },
  },
  mounted() {
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
