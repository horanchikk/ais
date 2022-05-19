const API_URL = "http://localhost:8000/";

/**
 * Отправляет GET запрос на сервер
 */
async function sendGET(url) {
  const req = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json; charset=utf-8",
    },
  });
  const result = await req.json();
  result["status"] = req.status;
  return result;
}

/**
 * Отправляет POST запрос на сервер
 */
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
  /**
   * Продажа билета
   * @param {int} film_id уникальный идентификатор фильма
   * @param {string} login логин пользователя
   * @param {string} password пароль пользователя
   */
  async sellTicket(film_id, login, password) {
    return await sendPOST(`${API_URL}users/sell_ticket`, {
      login: login,
      password: password,
      film_id: film_id,
    });
  },
  /**
   * Авторизация пользователя
   * @param {string} login логин пользователя
   * @param {string} passwd пароль пользователя
   */
  async login(login, passwd) {
    return await sendPOST(`${API_URL}users/login`, {
      login: login,
      password: passwd,
    });
  },
  /**
   * Регистрация пользователя.
   * @param {string} login логин пользователя
   * @param {string} passwd пароль пользователя
   * @param {float} discount скидка на фильмы. Требует access_key
   * @param {string} role роль пользователя. Требует access_key
   * @param {string} access_key админ-ключ.
   */
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
