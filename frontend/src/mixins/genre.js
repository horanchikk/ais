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
  Ужасы: "p-button-danger",
  Триллер: "p-button-primary",
  Комедия: "p-button-warning",
  Романтика: "p-button-secondary",
  Мелодрамма: "p-button-secondary",
  Драма: "p-button-primary",
  Фэнтези: "p-button-success",
  Фантастика: "p-button-info",
};

export default {
  /**
   * Детектит цвет для тега по его жанру.
   */
  methods: {
    detectGenre(genre) {
      if (genre in genres) {
        return genres[genre];
      } else {
        return "p-button-primary";
      }
    },
  },
};
