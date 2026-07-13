// Funciones Globales

// Formatear moneda
function formatCurrency(amount, currencySymbol = 'RD$') {
    return `${currencySymbol} ${parseFloat(amount).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')}`;
}

// Formatear fecha
function formatDate(date, format = 'DD/MM/YYYY') {
    const d = new Date(date);
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    const hours = String(d.getHours()).padStart(2, '0');
    const minutes = String(d.getMinutes()).padStart(2, '0');
    
    if (format === 'DD/MM/YYYY') {
        return `${day}/${month}/${year}`;
    } else if (format === 'DD/MM/YYYY HH:mm') {
        return `${day}/${month}/${year} ${hours}:${minutes}`;
    }
    return `${day}/${month}/${year}`;
}

// Mostrar notificación
function showNotification(message, type = 'success', duration = 5000) {
    const colors = {
        success: '#22c55e',
        error: '#ef4444',
        warning: '#f59e0b',
        info: '#3b82f6'
    };
    
    const toast = document.createElement('div');
    toast.className = 'position-fixed bottom-0 end-0 p-3';
    toast.style.zIndex = '1050';
    toast.innerHTML = `
        <div class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header" style="border-bottom: 3px solid ${colors[type] || colors.info}">
                <strong class="me-auto">
                    <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
                    ${type.charAt(0).toUpperCase() + type.slice(1)}
                </strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, duration);
}

// Confirmación con modal
function confirmAction(message, callback) {
    const confirmModal = document.getElementById('confirmModal');
    if (confirmModal) {
        const modal = new bootstrap.Modal(confirmModal);
        document.getElementById('confirmMessage').textContent = message;
        
        document.getElementById('confirmYes').onclick = function() {
            modal.hide();
            if (typeof callback === 'function') {
                callback();
            }
        };
        
        modal.show();
    } else {
        if (confirm(message)) {
            if (typeof callback === 'function') {
                callback();
            }
        }
    }
}

// Validar formulario antes de enviar
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    // Validar email
    const emailInput = form.querySelector('input[type="email"]');
    if (emailInput && emailInput.value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailInput.value)) {
            emailInput.classList.add('is-invalid');
            isValid = false;
        }
    }
    
    return isValid;
}

// Cargar select dependiente
function loadDependentSelect(url, params, targetId, callback) {
    $.ajax({
        url: url,
        method: 'GET',
        data: params,
        success: function(response) {
            const select = document.getElementById(targetId);
            if (select) {
                select.innerHTML = '<option value="">Seleccionar...</option>';
                if (Array.isArray(response)) {
                    response.forEach(item => {
                        const option = document.createElement('option');
                        option.value = item.id;
                        option.textContent = item.name || item.text;
                        select.appendChild(option);
                    });
                }
                
                if (typeof callback === 'function') {
                    callback(response);
                }
            }
        },
        error: function() {
            showNotification('Error al cargar los datos', 'error');
        }
    });
}

// Exportar datos a CSV
function exportToCSV(data, filename = 'reporte.csv') {
    if (!data || !data.length) {
        showNotification('No hay datos para exportar', 'warning');
        return;
    }
    
    const headers = Object.keys(data[0]);
    let csv = headers.join(',') + '\n';
    
    data.forEach(row => {
        const values = headers.map(header => {
            let value = row[header] || '';
            if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
                value = `"${value.replace(/"/g, '""')}"`;
            }
            return value;
        });
        csv += values.join(',') + '\n';
    });
    
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Inicializar tooltips y popovers
document.addEventListener('DOMContentLoaded', function() {
    // Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
    
    // Auto dismiss de alertas
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const closeBtn = alert.querySelector('.btn-close');
            if (closeBtn) {
                closeBtn.click();
            }
        }, 5000);
    });
});

// Ocultar mensajes de error al escribir
document.addEventListener('input', function(e) {
    if (e.target.classList.contains('is-invalid')) {
        e.target.classList.remove('is-invalid');
    }
});

// Confirmar eliminación en enlaces
document.addEventListener('click', function(e) {
    const link = e.target.closest('[data-confirm]');
    if (link) {
        e.preventDefault();
        const message = link.getAttribute('data-confirm') || '¿Está seguro de realizar esta acción?';
        if (confirm(message)) {
            window.location.href = link.href;
        }
    }
});