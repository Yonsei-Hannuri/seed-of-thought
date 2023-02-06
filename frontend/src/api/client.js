import axios from 'axios';
import getCookieValue from '../modules/getCookieValue';

const client = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  withCredentials: true,
});

client.interceptors.request.use((config) => {
  const csrfToken = getCookieValue(document.cookie, 'csrftoken');
  config.headers['X-CSRFToken'] = csrfToken;
  return config;
});

export default client;
