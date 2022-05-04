<template>
  <div class="h-full w-full text-white">
    <VirtualScroller
      :items="films"
      :item-size="1"
      style="height: 100%"
      v-if="!regForm"
    >
      <template v-slot:item="film">
        <!-- bg-gray-200 rounded-lg shadow-lg -->
        <!-- mx-16 my-5  -->
        <div class="flex gap-5 p-4 mx-16 my-5 bg-gray-700 rounded-lg">
          <div class="h-full justify-center items-center">
            <img
              :src="film.item.imgUrl"
              :alt="film.item.imgUrl"
              class="text-sm h-96 rounded-lg"
            />
          </div>
          <div class="flex flex-col justify-between gap-3 w-3/4">
            <div class="flex flex-col gap-2">
              <p class="text-4xl">{{ film.item.name }}</p>
              <div class="typeFilms">
                <Button
                  v-for="genre in film.item.type"
                  :key="genre"
                  :label="genre"
                  :class="'p-button-outlined w-fit' + this.detectGenre(genre)"
                  style="margin: 3px"
                />
              </div>
            </div>
            <p class="text-2xl cursor-default">{{ film.item.description }}</p>
            <Button
              label="Купить билет"
              class="p-button-raised p-button-success"
              @click="displayBuy = true"
            />
          </div>
        </div>
      </template>
    </VirtualScroller>

    <!-- Get Ticket -->
    <div
      class="h-full w-full flex justify-center items-center"
      v-else-if="buyTicket"
    >
      <div class="h-5/6 w-5/6">
        <div
          class="h-full w-full flex flex-col rounded-md"
          style="background-color: rgb(31, 31, 31)"
        >
          <h1 class="text-white text-center text-2xl p-2">
            Бронирование билетов на фильм "{{ filmName }}"
          </h1>
          <div
            class="flex flex-auto flex-col justify-center items-center p-2"
          ></div>
        </div>
      </div>
    </div>

    <!-- Reg Form -->
    <div
      class="h-full w-full flex justify-center items-center"
      v-else-if="regForm"
    >
      <div class="h-5/6 w-5/6">
        <div
          class="h-full w-full flex flex-col rounded-md"
          style="background-color: rgb(31, 31, 31)"
        >
          <div class="flex flex-auto justify-center items-center p-2"></div>
        </div>
      </div>
    </div>

    <div v-else>errrrrror</div>
    <Dialog v-model:visible="displayBuy" :modal="true" :draggable="false">
      <template #header>
        <div class="flex flex-col" v-if="state == 1">
          <h1 class="text-xl">Покупка билета</h1>
          <br />
          <h2 class="text-sm">Выберите дату</h2>
        </div>
      </template>
      <div v-if="state == 1">
        <div class="confirmation-content">
          <Calendar
            v-model="selectedDate"
            :inline="true"
            :showWeek="true"
            :showButtonBar="true"
            :date-format="'dd.mm.yy'"
            :touchUI="false"
          />
        </div>
      </div>

      <div v-if="state == 2">
        <div class="confirmation-content">иди нахуй</div>
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
            @click="state = 2"
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
import VirtualScroller from "primevue/virtualscroller";
import Calendar from "primevue/calendar";
import InputText from "primevue/inputtext";
import Dialog from "primevue/dialog";
import Genre from "../mixins/genre.js";
import CinemaAPI from "../mixins/cinemaApi.js";

export default {
  data() {
    return {
      regForm: false,
      displayBuy: false,
      displaytest: false,
      filmName: "nigger",
      selectedDate: null,
      state: 1,
      films: [
        {
          name: "САЛО",
          type: ["Комедия", "Драма", "Романтика", "Ужасы", "Триллер"],
          description:
            "At vero rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.",
          imgUrl:
            "https://i.pinimg.com/originals/1f/3f/e9/1f3fe9eb11b059bbeabc578f01beeccf.jpg",
        },
        {
          name: "Иная",
          type: ["Триллер", "Ужасы"],
          description:
            "On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. ",
          imgUrl:
            "https://i.pinimg.com/736x/d7/62/d9/d762d93e4a541f84f758d4c28fd5f19c--wish-list-otaku.jpg",
        },
        {
          name: "Иностранец 2",
          type: ["Боевик"],
          description:
            "These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best",
          imgUrl:
            "https://i.pinimg.com/originals/1f/3f/e9/1f3fe9eb11b059bbeabc578f01beeccf.jpg",
        },
        {
          name: "Сало 2",
          type: ["Боевик"],
          description:
            "every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures ",
          imgUrl:
            "https://i.pinimg.com/736x/d7/62/d9/d762d93e4a541f84f758d4c28fd5f19c--wish-list-otaku.jpg",
        },
        {
          name: "Иная 2",
          type: ["Ужасы"],
          description:
            "Interdum et malesuada fames ac ante ipsum primis in faucibus. Mauris nisl libero, volutpat sed varius at, semper vel massa. Fusce a mauris justo. Duis tempus fermentum commodo. Integer molestie bibendum leo, et semper lectus pulvinar nec. Duis hendrerit nibh eget facilisis bibendum. Proin libero justo, porta ac dolor ultrices, fermentum convallis tellus.",
          imgUrl:
            "https://i.pinimg.com/736x/d7/62/d9/d762d93e4a541f84f758d4c28fd5f19c--wish-list-otaku.jpg",
        },
        {
          name: "Иная 3",
          type: ["Ужасы"],
          description:
            "Fusce lacus sem, aliquam sed rutrum et, molestie vel diam. Duis nec vulputate diam, ut molestie velit. Maecenas ex sem, tincidunt ut turpis vitae, commodo pellentesque ipsum. Cras dolor erat, fermentum nec luctus non, fringilla eget mauris. Interdum et malesuada fames ac ante ipsum primis in faucibus. Duis pretium feugiat dignissim. Morbi non placerat leo. Nullam massa orci, posuere quis lobortis quis, pretium sed nisi. Aliquam finibus sem ex, vel dictum urna luctus quis. Maecenas laoreet finibus pellentesque. Nullam ex urna, lacinia eu semper in, convallis sed metus. Sed non consequat turpis. Interdum et malesuada fames ac ante ipsum primis in faucibus.",
          imgUrl:
            "https://i.pinimg.com/originals/1f/3f/e9/1f3fe9eb11b059bbeabc578f01beeccf.jpg",
        },
        {
          name: "Имя фильма3",
          type: ["Ужасы"],
          description:
            "Suspendisse ac ante et dolor porta fringilla. Etiam tempor facilisis fermentum. Nam molestie arcu et auctor viverra. Sed ultricies mauris augue, eu dignissim urna tempor eget. Phasellus consectetur faucibus risus. Cras semper scelerisque eros eget ornare. Nullam augue dolor, porttitor quis urna ut, maximus dignissim ex. In eget vehicula enim. Donec id lorem sit amet enim interdum dapibus vitae ac urna. Aenean vitae consectetur urna. Curabitur eget suscipit turpis, ac suscipit est. Proin quis diam a ligula semper consectetur eu eget tellus. Nulla blandit augue at eros aliquet ornare. Aenean nisi ante, porttitor finibus dui a, imperdiet elementum lacus. Proin vulputate libero eu neque commodo eleifend. Aliquam erat volutpat.",
          imgUrl:
            "https://i.pinimg.com/originals/1f/3f/e9/1f3fe9eb11b059bbeabc578f01beeccf.jpg",
        },
      ],
    };
  },
  components: {
    Button,
    VirtualScroller,
    Calendar,
    InputText,
    Dialog,
  },
  mixins: [Genre, CinemaAPI],
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
