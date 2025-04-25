// api.js - API service for the Debate Stimulator frontend
import axios from 'axios';
import { mockApi } from './mockApi';

// Flag to determine whether to use the mock API or real backend
const USE_MOCK_API = true;

// Create axios instance for the real API
const apiClient = axios.create({
  baseURL: '/',
  headers: {
    'Content-Type': 'application/json',
  },
});

// API service that either uses the real backend or mock data
const apiService = {
  // Start a new debate
  startDebate: async (config) => {
    if (USE_MOCK_API) {
      return mockApi.startDebate(config);
    }
    const response = await apiClient.post('/start-debate', config);
    return response.data;
  },
  
  // Get debate status
  getDebateStatus: async (debateId) => {
    if (USE_MOCK_API) {
      return mockApi.getDebateStatus(debateId);
    }
    const response = await apiClient.get(`/debates/${debateId}/status`);
    return response.data;
  },
  
  // Get next speaker
  getNextSpeaker: async (debateId) => {
    if (USE_MOCK_API) {
      return mockApi.getNextSpeaker(debateId);
    }
    const response = await apiClient.get(`/debates/${debateId}/next-speaker`);
    return response.data;
  },
  
  // Submit speech
  submitSpeech: async (debateId, speechInput) => {
    if (USE_MOCK_API) {
      return mockApi.submitSpeech(debateId, speechInput);
    }
    const response = await apiClient.post(`/debates/${debateId}/speech`, speechInput);
    return response.data;
  },
  
  // Generate AI speech
  generateAISpeech: async (debateId) => {
    if (USE_MOCK_API) {
      return mockApi.generateAISpeech(debateId);
    }
    const response = await apiClient.post(`/debates/${debateId}/ai-speech`);
    return response.data;
  },
  
  // Get all speeches
  getSpeeches: async (debateId) => {
    if (USE_MOCK_API) {
      return mockApi.getSpeeches(debateId);
    }
    const response = await apiClient.get(`/debates/${debateId}/speeches`);
    return response.data;
  },
  
  // Process audio
  processAudio: async (audioBase64) => {
    if (USE_MOCK_API) {
      return mockApi.processAudio(audioBase64);
    }
    const response = await apiClient.post(`/debates/audio`, { audio_base64: audioBase64 });
    return response.data;
  }
};

export default apiService;
