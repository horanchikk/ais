<template>
  <div class="h-full w-full text-white">
    <VirtualScroller :items="films" :item-size="1" style="height: 100%">
      <template v-slot:item="film">
        <!-- bg-gray-200 rounded-lg shadow-lg -->
        <div class="flex gap-5 p-4 mx-36 my-10 bg-gray-900">
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
                  :class="'p-button-outlined ' + this.detectGenre(genre)"
                />
              </div>
            </div>
            <p class="text-2xl">{{ film.item.description }}</p>
            <Button
              label="Купить билет"
              class="p-button-raised p-button-success"
            />
          </div>
        </div>
      </template>
    </VirtualScroller>
  </div>
</template>

<script>
import Button from "primevue/button";
import VirtualScroller from "primevue/virtualscroller";
import Genre from "../mixins/genre.js";

export default {
  data() {
    return {
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
          name: "Имя фильма2",
          type: ["Боевик"],
          description:
            "These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best",
          imgUrl:
            "https://i.pinimg.com/originals/1f/3f/e9/1f3fe9eb11b059bbeabc578f01beeccf.jpg",
        },
        {
          name: "Имя фильма2",
          type: ["Боевик"],
          description:
            "every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures ",
          imgUrl:
            "https://i.pinimg.com/736x/d7/62/d9/d762d93e4a541f84f758d4c28fd5f19c--wish-list-otaku.jpg",
        },
        {
          name: "Имя фильма3",
          type: ["Ужасы"],
          description: "Описание фильма3",
          imgUrl:
            "https://i.pinimg.com/736x/d7/62/d9/d762d93e4a541f84f758d4c28fd5f19c--wish-list-otaku.jpg",
        },
        {
          name: "Имя фильма3",
          type: ["Ужасы"],
          description: "Описание фильма3",
          imgUrl:
            "https://i.pinimg.com/originals/1f/3f/e9/1f3fe9eb11b059bbeabc578f01beeccf.jpg",
        },
        {
          name: "Имя фильма3",
          type: ["Ужасы"],
          description: "Описание фильма3",
          imgUrl:
            "https://i.pinimg.com/originals/1f/3f/e9/1f3fe9eb11b059bbeabc578f01beeccf.jpg",
        },
      ],
    };
  },
  components: {
    Button,
    VirtualScroller,
  },
  mixins: [Genre],
};
</script>

<style />
