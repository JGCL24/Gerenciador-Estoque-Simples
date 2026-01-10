/**
 * Configuração e utilitários da API
 */
const API = {
    getUrl: () => {
        const url = document.getElementById('apiUrl')?.value || 'http://localhost:8000';
        return url.endsWith('/') ? url.slice(0, -1) : url;
    },

    

    async request(endpoint, options = {}) {
        const url = `${this.getUrl()}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };
        
        const mergedOptions = { ...defaultOptions, ...options };
        if (options.body && typeof options.body === 'object') {
            mergedOptions.body = JSON.stringify(options.body);
        }

        try {
            const response = await fetch(url, mergedOptions);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.detail || `Erro ${response.status}: ${response.statusText}`);
            }
            
            return data;
        } catch (error) {
            throw error;
        }
    },

    async testConnection() {
        try {
            const response = await fetch(`${this.getUrl()}/health`);
            const data = await response.json();
            return data.status === 'healthy';
        } catch (error) {
            return false;
        }
    }
};
