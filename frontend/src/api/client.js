import axios from 'axios';
import address from '../config/address.json';
import getCookieValue from '../modules/getCookieValue';

const client = axios.create({
  baseURL: address.back,
  withCredentials: true,
});

client.interceptors.request.use((config) => {
  const csrfToken = getCookieValue(document.cookie, 'csrftoken');
  config.headers['X-CSRFToken'] = csrfToken;
  return config;
});

export default client;
