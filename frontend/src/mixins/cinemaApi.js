import Toast from "primevue/toast";
import ToastService from "primevue/toastservice";
const API_URL = "http://localhost:8000/";

async function sendGET(url) {
  const req = await fetch(url);
  const result = await req.json();
  result["status"] = req.status;
  return result;
}

async function sendPOST(url, data) {
  const req = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json; charset=utf-8",
    },
    body: JSON.stringify(data),
  });
  const result = await req.json();
  result["status"] = req.status;
  return result;
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
  /**
   * Покупка билета
   * @param {int} film_id уникальный идентификатор фильма.
   * @param {int} user_id уникальный идентификатор пользователя.
   * @param {int} date дата, только в unix.
   */
  async buyTicket(film_id, user_id, date) {
    return await sendGET(
      `${API_URL}films/buy?film_id=${film_id}&user_id=${user_id}&date=${date}`
    );
  },
  async login(login, passwd) {
    return await sendPOST(`${API_URL}users/login`, {
      login: login,
      password: passwd,
    });
  },

  async reg(login, passwd, discount = 0.0, role = "client", access_key = "") {
    return await sendPOST(`${API_URL}users/reg`, {
      login: login,
      password: passwd,
      discount: discount,
      role: role,
      access_key: access_key,
    });
  },
};
