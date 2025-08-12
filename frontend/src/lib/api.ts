import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_FOOD_API_BASE_URL || 'http://localhost:8000/api/v0';

export const api = axios.create({
  baseURL: API_BASE_URL,
});