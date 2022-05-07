const API_URL = "http:localhost:8000/";

async function sendGET(url) {
  const req = await fetch(url);
  return await req.json();
}

async function sendPOST(url, data) {
  const req = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json; charset=utf-8'
    },
    body: data
  });
  return await req.json()
}

export default {
  /**
   * @returns список всех пользователей
   */
  async getAllUsers() {
    return await sendGET(`${API_URL}users/getall`);
  },
  /**
   * @returns список всех фильмов
   */
  async getAllFilms() {
    return await sendGET(`${API_URL}films/getall`);
  },
  /**
   * Возвращает пользователя по его ID
   * @param {int} id уникальный идентификатор пользователя.
   * @returns объект пользователя
   */
  async getUserById(id) {
    return await sendGET(`${API_URL}users/get?user_id=${id}`);
  },
  /**
   * Возвращает фильм по его ID
   * @param {int} id уникальный идентификатор фильма.
   * @returns объект фильма
   */
  async getFilmById(id) {
    return await sendGET(`${API_URL}films/get?film_id=${id}`);
  },
};
