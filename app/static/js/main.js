// ================================================
// JavaScript Principal
// ================================================

console.log('[OK] Biblioteca iniciada correctamente');

// Función para mostrar alertas
function showAlert(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alert, container.firstChild);
        
        // Auto-desaparecer después de 5 segundos
        setTimeout(() => {
            alert.remove();
        }, 5000);
    }
}

// Confirmación para eliminar
function confirmDelete(itemName) {
    return confirm(`¿Estás seguro de que deseas eliminar "${itemName}"?`);
}

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    console.log('📚 DOM cargado');
    // Aquí van las inicializaciones del sitio
});
