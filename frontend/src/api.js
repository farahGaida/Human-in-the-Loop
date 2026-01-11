import axios from 'axios';

// Set up the base configuration for Axios to communicate with our FastAPI server
const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
});

export const cvService = {
    // Get all CVs that still need manual validation (status 'pending')
    getPending: async () => {
        const response = await api.get('/extractions/');
        return response.data;
    },
    // Send the human corrections and time tracking data to the backend
    submitCorrection: async (id, data) => {
        const response = await api.post(`/extractions/${id}/correct`, data);
        return response.data;
    },

    // Fetch analytics data from the metrics route for the dashboard
    getMetrics: async () => {
        const response = await api.get('/metrics/'); 
        return response;
    }
};

export default api;