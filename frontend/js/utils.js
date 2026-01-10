/**
 * Funções utilitárias
 */

// Funções de UI
const UI = {
    getTabName: function(tabId) {
        const names = {
            'usuarios': 'Usuários',
            'clientes': 'Clientes',
            'campos': 'Campos',
            'reservas': 'Reservas',
            'produtos': 'Produtos',
            'estoque': 'Estoque',
            'mesas': 'Mesas',
            'comandas': 'Comandas',
            'compras': 'Compras',
            'pagamentos': 'Pagamentos'
        };
        return names[tabId] || tabId;
    },

    showTab: function(tabName, event) {
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.querySelectorAll('.tab').forEach(tab => {
            tab.classList.remove('active');
        });
        const tabElement = document.getElementById(tabName);
        if (tabElement) {
            tabElement.classList.add('active');
        }
        // Ativar a aba correspondente
        if (event && event.target) {
            event.target.classList.add('active');
        } else {
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(tab => {
                if (tab.textContent.trim() === this.getTabName(tabName)) {
                    tab.classList.add('active');
                }
            });
        }
    },

    showMessage: function(text, type = 'success') {
        const msg = document.getElementById('message');
        if (msg) {
            msg.textContent = text;
            msg.className = `message ${type} show`;
            setTimeout(() => {
                msg.classList.remove('show');
            }, 5000);
        }
    },

    updateConnectionStatus: function(status, message) {
        const statusEl = document.getElementById('connectionStatus');
        if (statusEl) {
            statusEl.textContent = message;
            statusEl.style.color = status ? 'green' : 'red';
        }
    },

    clearForm: function(formId) {
        const form = document.getElementById(formId);
        if (form) {
            form.reset();
        } else {
            // Limpar campos específicos
            const inputs = document.querySelectorAll(`#${formId} input, #${formId} select`);
            inputs.forEach(input => {
                if (input.type === 'checkbox' || input.type === 'radio') {
                    input.checked = false;
                } else {
                    input.value = '';
                }
            });
        }
    }
};

// Função global para mostrar aba (para onclick nos botões)
function showTab(tabName) {
    UI.showTab(tabName, event);
}

// Função para testar conexão
async function testConnection() {
    const connected = await API.testConnection();
    if (connected) {
        UI.updateConnectionStatus(true, '✓ Conectado');
        UI.showMessage('Conexão estabelecida com sucesso!', 'success');
    } else {
        UI.updateConnectionStatus(false, '✗ Erro');
        UI.showMessage('Erro ao conectar com a API', 'error');
    }
}
