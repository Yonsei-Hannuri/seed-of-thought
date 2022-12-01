import axios from 'axios';
import address from '../config/address.json';

const client = axios.create({
  baseURL: address.back,
  withCredentials: true,
});

export default client;
