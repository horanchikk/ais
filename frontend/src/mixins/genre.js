/**
 * danger - красный
 * primary - серый
 * warning - желтый
 * secondary - розовый
 * success - зеленый
 * info - синий
 * help - фиолетовый
 */
const genres = {
  ужасы: "p-button-danger",
  триллер: "p-button-primary",
  комедия: "p-button-warning",
  романтика: "p-button-secondary",
  мелодрамма: "p-button-secondary",
  драма: "p-button-primary",
  фэнтези: "p-button-success",
  фантастика: "p-button-info",
};

export default {
  /**
   * Детектит цвет для тега по его жанру.
   */
  methods: {
    detectGenre(genre) {
      let g = genre.toLowerCase();
      if (g in genres) {
        return genres[g];
      } else {
        return "p-button-primary";
      }
    },
  },
};
