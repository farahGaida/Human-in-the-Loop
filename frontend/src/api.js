import axios from 'axios';

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
});

export const cvService = {
    // Récupérer les CV non corrigés
    getPending: async () => {
        const response = await api.get('/extractions/');
        return response.data;
    },
    // Envoyer la correction
    submitCorrection: async (id, data) => {
        const response = await api.post(`/extractions/${id}/correct`, data);
        return response.data;
    },

    getMetrics: async () => {
        //  appelle routes/metrics.py
        const response = await api.get('/metrics/'); 
        return response; // On retourne l'objet réponse complet car MetricsDashboard utilise .data
    }
};

export default api;