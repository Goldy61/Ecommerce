/**
 * Admin Panel JavaScript functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeAdminFunctionality();
});

/**
 * Initialize admin functionality
 */
function initializeAdminFunctionality() {
    initializeDeleteButtons();
    initializeStatusUpdates();
    initializeFormValidation();
    initializeDataTables();
}

/**
 * Initialize delete confirmation buttons
 */
function initializeDeleteButtons() {
    const deleteButtons = document.querySelectorAll('.btn-delete, .delete-btn');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const itemName = this.getAttribute('data-item-name') || 'this item';
            const confirmMessage = `Are you sure you want to delete ${itemName}? This action cannot be undone.`;
            
            if (confirm(confirmMessage)) {
                // If it's a form button, submit the form
                const form = this.closest('form');
                if (form) {
                    form.submit();
                } else {
                    // If it's an AJAX delete
                    const deleteUrl = this.getAttribute('data-delete-url');
                    if (deleteUrl) {
                        performDelete(deleteUrl, this);
                    }
                }
            }
        });
    });
}

/**
 * Perform AJAX delete operation
 */
function performDelete(url, buttonElement) {
    buttonElement.disabled = true;
    buttonElement.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    
    ECommerce.makeAjaxRequest(url, {
        method: 'POST'
    })
    .then(response => {
        if (response.success) {
            ECommerce.showNotification(response.message, 'success');
            
            // Remove the row from table
            const row = buttonElement.closest('tr');
            if (row) {
                row.style.opacity = '0';
                setTimeout(() => {
                    row.remove();
                }, 300);
            }
        } else {
            ECommerce.showNotification(response.message, 'error');
        }
    })
    .catch(error => {
        ECommerce.showNotification('Failed to delete item', 'error');
    })
    .finally(() => {
        buttonElement.disabled = false;
        buttonElement.innerHTML = '<i class="fas fa-trash"></i>';
    });
}

/**
 * Initialize status update functionality
 */
function initializeStatusUpdates() {
    const statusSelects = document.querySelectorAll('.status-select');
    
    statusSelects.forEach(select => {
        select.addEventListener('change', function() {
            const orderId = this.getAttribute('data-order-id');
            const newStatus = this.value;
            
            if (orderId && newStatus) {
                updateOrderStatus(orderId, newStatus, this);
            }
        });
    });
}

/**
 * Update order status via AJAX
 */
function updateOrderStatus(orderId, newStatus, selectElement) {
    const originalValue = selectElement.getAttribute('data-original-value');
    selectElement.disabled = true;
    
    const data = {
        order_id: parseInt(orderId),
        status: newStatus
    };
    
    ECommerce.makeAjaxRequest('/admin/orders/update-status', {
        method: 'POST',
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.success) {
            ECommerce.showNotification(response.message, 'success');
            selectElement.setAttribute('data-original-value', newStatus);
            
            // Update status badge if exists
            const statusBadge = selectElement.closest('tr').querySelector('.status-badge');
            if (statusBadge) {
                statusBadge.className = `status-badge status-${newStatus}`;
                statusBadge.textContent = newStatus.charAt(0).toUpperCase() + newStatus.slice(1);
            }
        } else {
            ECommerce.showNotification(response.message, 'error');
            selectElement.value = originalValue;
        }
    })
    .catch(error => {
        ECommerce.showNotification('Failed to update status', 'error');
        selectElement.value = originalValue;
    })
    .finally(() => {
        selectElement.disabled = false;
    });
}

/**
 * Initialize form validation for admin forms
 */
function initializeFormValidation() {
    const adminForms = document.querySelectorAll('.admin-form');
    
    adminForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateAdminForm(form)) {
                e.preventDefault();
            }
        });
    });
}

/**
 * Validate admin form
 */
function validateAdminForm(form) {
    let isValid = true;
    
    // Clear previous errors
    const errorElements = form.querySelectorAll('.field-error');
    errorElements.forEach(error => error.remove());
    
    // Validate required fields
    const requiredFields = form.querySelectorAll('[required]');
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            showFieldError(field, 'This field is required');
            isValid = false;
        }
    });
    
    // Validate numeric fields
    const numericFields = form.querySelectorAll('input[type="number"]');
    numericFields.forEach(field => {
        if (field.value && isNaN(field.value)) {
            showFieldError(field, 'Please enter a valid number');
            isValid = false;
        }
        
        if (field.hasAttribute('min') && parseFloat(field.value) < parseFloat(field.getAttribute('min'))) {
            showFieldError(field, `Value must be at least ${field.getAttribute('min')}`);
            isValid = false;
        }
    });
    
    // Validate price fields
    const priceFields = form.querySelectorAll('input[name*="price"]');
    priceFields.forEach(field => {
        if (field.value && parseFloat(field.value) <= 0) {
            showFieldError(field, 'Price must be greater than 0');
            isValid = false;
        }
    });
    
    return isValid;
}

/**
 * Show field error message
 */
function showFieldError(field, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    errorDiv.style.cssText = `
        color: #dc3545;
        font-size: 0.875rem;
        margin-top: 0.25rem;
    `;
    
    field.parentNode.appendChild(errorDiv);
    field.style.borderColor = '#dc3545';
}

/**
 * Initialize data tables with search and pagination
 */
function initializeDataTables() {
    const searchInputs = document.querySelectorAll('.table-search');
    
    searchInputs.forEach(input => {
        const tableId = input.getAttribute('data-table');
        const table = document.getElementById(tableId);
        
        if (table) {
            input.addEventListener('input', ECommerce.debounce(function() {
                filterTable(table, this.value);
            }, 300));
        }
    });
}

/**
 * Filter table rows based on search term
 */
function filterTable(table, searchTerm) {
    const rows = table.querySelectorAll('tbody tr');
    const term = searchTerm.toLowerCase();
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(term) ? '' : 'none';
    });
}

/**
 * Initialize image preview for file uploads
 */
function initializeImagePreview() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    
    imageInputs.forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            const previewId = this.getAttribute('data-preview');
            const preview = document.getElementById(previewId);
            
            if (file && preview) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        });
    });
}

/**
 * Initialize bulk actions
 */
function initializeBulkActions() {
    const selectAllCheckbox = document.getElementById('select-all');
    const itemCheckboxes = document.querySelectorAll('.item-checkbox');
    const bulkActionSelect = document.getElementById('bulk-action');
    const bulkActionButton = document.getElementById('bulk-action-btn');
    
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            itemCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
            updateBulkActionButton();
        });
    }
    
    itemCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateBulkActionButton);
    });
    
    if (bulkActionButton) {
        bulkActionButton.addEventListener('click', function() {
            const selectedItems = Array.from(itemCheckboxes)
                .filter(cb => cb.checked)
                .map(cb => cb.value);
            
            const action = bulkActionSelect.value;
            
            if (selectedItems.length === 0) {
                ECommerce.showNotification('Please select items to perform bulk action', 'warning');
                return;
            }
            
            if (!action) {
                ECommerce.showNotification('Please select an action', 'warning');
                return;
            }
            
            if (confirm(`Are you sure you want to ${action} ${selectedItems.length} item(s)?`)) {
                performBulkAction(action, selectedItems);
            }
        });
    }
    
    function updateBulkActionButton() {
        const selectedCount = Array.from(itemCheckboxes).filter(cb => cb.checked).length;
        if (bulkActionButton) {
            bulkActionButton.textContent = `Apply to ${selectedCount} item(s)`;
            bulkActionButton.disabled = selectedCount === 0;
        }
    }
}

/**
 * Perform bulk action
 */
function performBulkAction(action, itemIds) {
    const data = {
        action: action,
        items: itemIds
    };
    
    ECommerce.makeAjaxRequest('/admin/bulk-action', {
        method: 'POST',
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.success) {
            ECommerce.showNotification(response.message, 'success');
            // Reload page or update UI
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            ECommerce.showNotification(response.message, 'error');
        }
    })
    .catch(error => {
        ECommerce.showNotification('Bulk action failed', 'error');
    });
}

/**
 * Initialize chart.js charts if available
 */
function initializeCharts() {
    // This would be implemented if Chart.js is included
    // Example: Sales chart, user registration chart, etc.
}

// Initialize additional features when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeImagePreview();
    initializeBulkActions();
    initializeCharts();
});

// Export functions for use in other files
window.Admin = {
    updateOrderStatus,
    performDelete,
    filterTable,
    validateAdminForm
};