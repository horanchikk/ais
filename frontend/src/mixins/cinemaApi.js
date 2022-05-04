const API_URL = "http:localhost:8000/";

async function sendReq(url) {
  const req = await fetch(url);
  return await req.json();
}

export default {
  async getAllUsers() {
    return await sendReq(`${API_URL}users/getall`);
  },
};
