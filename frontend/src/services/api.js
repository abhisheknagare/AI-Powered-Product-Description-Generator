// frontend/src/services/api.js
import axios from "axios";

const BASE_URL = "http://localhost:5000"; // Update if deployed

// Create a configured axios instance
const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Helper function to make POST requests
const makePostRequest = async (endpoint, data) => {
  const res = await apiClient.post(endpoint, data);
  return res.data;
};

export const generateDescription = async (product, tone, length, style) => {
  const data = await makePostRequest('/generate/description', {
    product,
    tone,
    length,
    style,
  });
  return data.description;
};

export const generateSEO = async (product, tone, length, style) => {
  const data = await makePostRequest('/generate/seo', {
    product,
    tone,
    length,
    style,
  });
  return data.seo;
};

export const generateMarketing = async (product, platform, tone, length, style) => {
  const data = await makePostRequest('/generate/marketing', {
    product,
    platform,
    tone,
    length,
    style,
  });
  return data.marketing;
};

export const generateImagePrompt = async (product) => {
  const data = await makePostRequest('/generate/image-prompt', {
    product,
  });
  return data.image_prompt;
};