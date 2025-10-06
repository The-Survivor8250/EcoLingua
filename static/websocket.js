/**
 * EcoLingua Real-time Development Features
 */

class EcoLinguaRealTime {
    constructor() {
        this.websocket = null;
        this.isConnected = false;
        this.dataBuffer = [];
        this.maxBufferSize = 1000;
        this.updateInterval = null;
        this.devMode = false;
        this.init();
    }
    
    init() {
        this.connectWebSocket();
        this.setupKeyboardShortcuts();
        this.startPerformanceMonitoring();
        this.initializeDevTools();
    }
    
    connectWebSocket() {
        // Check for ngrok configuration
        let wsUrl;
        if (window.NGROK_CONFIG) {
            wsUrl = window.NGROK_CONFIG.websocketUrl;
        } else {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            wsUrl = `${protocol}//${window.location.host}/ws`;
        }
        
        this.websocket = new WebSocket(wsUrl);
        
        this.websocket.onopen = () => {
            this.isConnected = true;
            this.showNotification('🔌 Real-time connection established', 'success');
        };
        
        this.websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleRealtimeData(data);
        };
        
        this.websocket.onclose = () => {
            this.isConnected = false;
            setTimeout(() => this.connectWebSocket(), 3000);
        };
    }
    
    handleRealtimeData(data) {
        this.dataBuffer.push({...data, clientTimestamp: Date.now()});
        if (this.dataBuffer.length > this.maxBufferSize) this.dataBuffer.shift();
        this.processRealtimeUpdate(data);
    }
    
    processRealtimeUpdate(data) {
        if (data.alerts && data.alerts.length > 0) {
            this.processAlerts(data.alerts);
        }
    }
    
    processAlerts(alerts) {
        alerts.forEach(alert => this.showAlert(alert));
    }
    
    showAlert(alert) {
        const alertsContainer = document.getElementById('alerts');
        if (!alertsContainer) return;
        
        const alertElement = document.createElement('div');
        alertElement.className = 'alert';
        alertElement.innerHTML = `
            <div class="alert-icon">⚠️</div>
            <div class="alert-content">
                <div class="alert-title">${alert.type.toUpperCase()}</div>
                <div class="alert-message">${alert.message}</div>
            </div>
        `;
        
        alertsContainer.insertBefore(alertElement, alertsContainer.firstChild);
        setTimeout(() => alertElement.remove(), 10000);
    }
    
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (event) => {
            if ((event.ctrlKey || event.metaKey) && event.shiftKey) {
                switch (event.key) {
                    case 'D': event.preventDefault(); this.toggleDevMode(); break;
                    case 'R': event.preventDefault(); this.refreshData(); break;
                    case 'S': event.preventDefault(); this.simulateData(); break;
                }
            }
        });
    }
    
    toggleDevMode() {
        this.devMode = !this.devMode;
        document.querySelectorAll('.dev-only').forEach(el => {
            el.style.display = this.devMode ? 'block' : 'none';
        });
        this.showNotification(`🔧 Dev mode ${this.devMode ? 'enabled' : 'disabled'}`, 'info');
    }
    
    refreshData() {
        const apiBase = window.NGROK_CONFIG ? window.NGROK_CONFIG.apiBase : '';
        fetch(`${apiBase}/api/current-status`)
            .then(response => response.json())
            .then(data => {
                this.handleRealtimeData(data);
                this.showNotification('🔄 Data refreshed', 'success');
            });
    }
    
    simulateData() {
        const mockData = {
            processed_data: {
                temperature: Math.random() * 10 + 20,
                humidity: Math.random() * 20 + 50,
                sound_level: Math.random() * 30 + 40
            },
            translation: "Simulated data: Nature responds to test conditions."
        };
        this.handleRealtimeData(mockData);
        this.showNotification('🧪 Test data simulated', 'info');
    }
    
    startPerformanceMonitoring() {
        this.updateInterval = setInterval(() => {
            const perfDisplay = document.getElementById('performanceMetrics');
            if (perfDisplay) {
                perfDisplay.innerHTML = `
                    <div>Buffer: ${this.dataBuffer.length}/${this.maxBufferSize}</div>
                    <div>Connected: ${this.isConnected ? 'Yes' : 'No'}</div>
                `;
            }
        }, 1000);
    }
    
    initializeDevTools() {
        // Dev tools disabled for production
    }
    
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed; top: 20px; right: 20px; padding: 12px 20px;
            border-radius: 8px; color: white; font-size: 14px; z-index: 10000;
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        `;
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 3000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.ecoRealTime = new EcoLinguaRealTime();
    
    const style = document.createElement('style');
    style.textContent = `
        .dev-tools-panel {
            position: fixed; bottom: 20px; left: 20px; width: 300px;
            background: rgba(15, 23, 42, 0.95); border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 12px; padding: 16px; font-size: 12px; z-index: 1000;
        }
        .dev-tools-header { color: #10b981; margin-bottom: 12px; }
        .performance-metrics {
            background: rgba(0, 0, 0, 0.3); padding: 8px; border-radius: 6px;
            margin-bottom: 12px; font-family: monospace; color: #cbd5e1;
        }
        .dev-actions { display: flex; gap: 8px; }
        .dev-actions button {
            background: rgba(16, 185, 129, 0.2); border: 1px solid #10b981;
            color: #10b981; padding: 6px 12px; border-radius: 6px; cursor: pointer;
        }
    `;
    document.head.appendChild(style);
});