/**
 * Цвета жанров
 */
const genres = {
  ужасы: "border-rose-700",
  триллер: "border-indigo-600",
  комедия: "border-yellow-300",
  романтика: "border-pink-500",
  мелодрамма: "border-fuchsia-700",
  драма: "border-violet-700",
  фэнтези: "border-green-500",
  фантастика: "border-cyan-600",
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
        return "border-gray-500";
      }
    },
  },
};
