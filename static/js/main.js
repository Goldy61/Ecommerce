/**
 * Main JavaScript file for E-Commerce website
 * Handles general functionality and UI interactions
 */

// DOM Content Loaded Event
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeComponents();
});

/**
 * Initialize all JavaScript components
 */
function initializeComponents() {
    initializeFlashMessages();
    initializeMobileMenu();
    initializeDropdowns();
    initializeFormValidation();
    initializeImageErrorHandling();
    refreshCartCountOnLoad();
    preloadImages();
    initializeThemeToggle();
    initializeSearchAutocomplete();
}

/**
 * Flash Messages Auto-hide
 */
function initializeFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        // Auto-hide after 5 seconds
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
}

/**
 * Mobile Menu Toggle
 */
function initializeMobileMenu() {
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const nav = document.querySelector('.nav');
    
    if (mobileToggle && nav) {
        mobileToggle.addEventListener('click', function() {
            nav.classList.toggle('active');
        });
    }
}

/**
 * Dropdown Menus
 */
function initializeDropdowns() {
    const dropdowns = document.querySelectorAll('.dropdown');
    
    dropdowns.forEach(dropdown => {
        const btn = dropdown.querySelector('.dropdown-btn');
        const content = dropdown.querySelector('.dropdown-content');
        
        if (btn && content) {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                content.style.display = content.style.display === 'block' ? 'none' : 'block';
            });
            
            // Close dropdown when clicking outside
            document.addEventListener('click', function(e) {
                if (!dropdown.contains(e.target)) {
                    content.style.display = 'none';
                }
            });
        }
    });
}

/**
 * Form Validation
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form)) {
                e.preventDefault();
            }
        });
    });
}

/**
 * Validate form fields
 */
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            showFieldError(field, 'This field is required');
            isValid = false;
        } else {
            clearFieldError(field);
        }
    });
    
    // Email validation
    const emailFields = form.querySelectorAll('input[type="email"]');
    emailFields.forEach(field => {
        if (field.value && !isValidEmail(field.value)) {
            showFieldError(field, 'Please enter a valid email address');
            isValid = false;
        }
    });
    
    // Password confirmation
    const passwordField = form.querySelector('input[name="password"]');
    const confirmField = form.querySelector('input[name="confirm_password"]');
    
    if (passwordField && confirmField && passwordField.value !== confirmField.value) {
        showFieldError(confirmField, 'Passwords do not match');
        isValid = false;
    }
    
    return isValid;
}

/**
 * Show field error
 */
function showFieldError(field, message) {
    clearFieldError(field);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    errorDiv.style.color = '#dc3545';
    errorDiv.style.fontSize = '0.875rem';
    errorDiv.style.marginTop = '0.25rem';
    
    field.parentNode.appendChild(errorDiv);
    field.style.borderColor = '#dc3545';
}

/**
 * Clear field error
 */
function clearFieldError(field) {
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
    field.style.borderColor = '';
}

/**
 * Email validation
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Image Error Handling with better fallbacks
 */
function initializeImageErrorHandling() {
    const images = document.querySelectorAll('img');
    
    images.forEach(img => {
        // Set up error handling
        img.addEventListener('error', function() {
            console.log('Image failed to load:', this.src);
            
            // Try placeholder.jpg first
            if (!this.src.includes('placeholder.jpg')) {
                this.src = '/static/images/placeholder.jpg';
                return;
            }
            
            // If placeholder also fails, hide image and show CSS fallback
            this.style.display = 'none';
            const parent = this.closest('.product-image, .hero-image, .category-card');
            if (parent) {
                parent.classList.add('image-error');
            }
        });
        
        // Handle images that load but are invalid
        img.addEventListener('load', function() {
            if (this.naturalWidth === 0 || this.naturalHeight === 0) {
                this.dispatchEvent(new Event('error'));
            }
        });
    });
}

/**
 * Preload critical images
 */
function preloadImages() {
    const criticalImages = [
        '/static/images/placeholder.jpg',
        '/static/images/hero-image.jpg'
    ];
    
    criticalImages.forEach(src => {
        const img = new Image();
        img.src = src;
    });
}

/**
 * Theme Toggle Functionality
 */
function initializeThemeToggle() {
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    const themeIcon = document.getElementById('theme-icon');
    const body = document.body;
    
    if (!themeToggleBtn || !themeIcon) return;
    
    // Check for saved theme preference or default to light mode
    const savedTheme = localStorage.getItem('theme') || 'light';
    
    // Apply saved theme
    if (savedTheme === 'dark') {
        body.classList.add('dark-theme');
        themeIcon.className = 'fas fa-sun';
        themeToggleBtn.title = 'Toggle Light Mode (Ctrl+Shift+T)';
    } else {
        body.classList.remove('dark-theme');
        themeIcon.className = 'fas fa-moon';
        themeToggleBtn.title = 'Toggle Dark Mode (Ctrl+Shift+T)';
    }
    
    // Theme toggle function
    function toggleTheme() {
        const isDark = body.classList.contains('dark-theme');
        
        if (isDark) {
            // Switch to light theme
            body.classList.remove('dark-theme');
            themeIcon.className = 'fas fa-moon';
            themeToggleBtn.title = 'Toggle Dark Mode (Ctrl+Shift+T)';
            localStorage.setItem('theme', 'light');
            animateThemeTransition('light');
        } else {
            // Switch to dark theme
            body.classList.add('dark-theme');
            themeIcon.className = 'fas fa-sun';
            themeToggleBtn.title = 'Toggle Light Mode (Ctrl+Shift+T)';
            localStorage.setItem('theme', 'dark');
            animateThemeTransition('dark');
        }
    }
    
    // Theme toggle click handler
    themeToggleBtn.addEventListener('click', toggleTheme);
    
    // Keyboard shortcut (Ctrl+Shift+T)
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.shiftKey && e.key === 'T') {
            e.preventDefault();
            toggleTheme();
        }
    });
}

/**
 * Animate theme transition
 */
function animateThemeTransition(theme) {
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    const themeIcon = document.getElementById('theme-icon');
    
    if (!themeToggleBtn || !themeIcon) return;
    
    // Add rotation animation to button
    themeToggleBtn.style.transform = 'rotate(360deg)';
    
    // Add scale animation to icon
    themeIcon.style.transform = 'scale(0)';
    
    setTimeout(() => {
        themeIcon.style.transform = 'scale(1)';
    }, 150);
    
    setTimeout(() => {
        themeToggleBtn.style.transform = 'rotate(0deg)';
    }, 300);
    
    // Show notification
    showNotification(
        `Switched to ${theme} theme`, 
        'success'
    );
}

/**
 * Get current theme
 */
function getCurrentTheme() {
    return document.body.classList.contains('dark-theme') ? 'dark' : 'light';
}

/**
 * Set theme programmatically
 */
function setTheme(theme) {
    const body = document.body;
    const themeIcon = document.getElementById('theme-icon');
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    
    if (theme === 'dark') {
        body.classList.add('dark-theme');
        if (themeIcon) themeIcon.className = 'fas fa-sun';
        if (themeToggleBtn) themeToggleBtn.title = 'Toggle Light Mode';
    } else {
        body.classList.remove('dark-theme');
        if (themeIcon) themeIcon.className = 'fas fa-moon';
        if (themeToggleBtn) themeToggleBtn.title = 'Toggle Dark Mode';
    }
    
    localStorage.setItem('theme', theme);
}

/**
 * Show loading spinner
 */
function showLoading(element) {
    const spinner = document.createElement('div');
    spinner.className = 'loading-spinner';
    spinner.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    
    element.appendChild(spinner);
}

/**
 * Hide loading spinner
 */
function hideLoading(element) {
    const spinner = element.querySelector('.loading-spinner');
    if (spinner) {
        spinner.remove();
    }
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button class="close-notification" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 5px;
        color: white;
        z-index: 10000;
        display: flex;
        align-items: center;
        justify-content: space-between;
        min-width: 300px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    
    // Set background color based on type
    switch(type) {
        case 'success':
            notification.style.backgroundColor = '#28a745';
            break;
        case 'error':
            notification.style.backgroundColor = '#dc3545';
            break;
        case 'warning':
            notification.style.backgroundColor = '#ffc107';
            notification.style.color = '#212529';
            break;
        default:
            notification.style.backgroundColor = '#17a2b8';
    }
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }, 5000);
}

/**
 * Format currency
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

/**
 * Debounce function for search
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * AJAX helper function
 */
function makeAjaxRequest(url, options = {}) {
    const defaultOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    const config = { ...defaultOptions, ...options };
    
    return fetch(url, config)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error('AJAX request failed:', error);
            showNotification('An error occurred. Please try again.', 'error');
            throw error;
        });
}

/**
 * Update cart count in header
 */
function updateCartCount(count) {
    const cartCountElement = document.getElementById('cart-count');
    if (cartCountElement) {
        cartCountElement.textContent = count;
        
        // Hide cart count if 0
        if (count === 0) {
            cartCountElement.style.display = 'none';
        } else {
            cartCountElement.style.display = 'inline';
        }
        
        // Add animation
        cartCountElement.style.transform = 'scale(1.2)';
        setTimeout(() => {
            cartCountElement.style.transform = 'scale(1)';
        }, 200);
    }
}

/**
 * Refresh cart count on page load
 */
function refreshCartCountOnLoad() {
    const cartCountElement = document.getElementById('cart-count');
    if (cartCountElement) {
        // Make AJAX request to get current cart count
        makeAjaxRequest('/api/cart/count')
            .then(response => {
                updateCartCount(response.cart_count);
            })
            .catch(error => {
                console.log('Cart count refresh failed (user may not be logged in)');
                // If request fails (user not logged in), hide cart count
                cartCountElement.style.display = 'none';
            });
    }
}

/**
 * Smooth scroll to element
 */
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

/**
 * Initialize tooltips (if needed)
 */
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.getAttribute('data-tooltip');
            tooltip.style.cssText = `
                position: absolute;
                background: #333;
                color: white;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 0.875rem;
                z-index: 10001;
                pointer-events: none;
            `;
            
            document.body.appendChild(tooltip);
            
            // Position tooltip
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + 'px';
            tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
        });
        
        element.addEventListener('mouseleave', function() {
            const tooltip = document.querySelector('.tooltip');
            if (tooltip) {
                tooltip.remove();
            }
        });
    });
}

// Export functions for use in other files
window.ECommerce = {
    showNotification,
    formatCurrency,
    makeAjaxRequest,
    updateCartCount,
    showLoading,
    hideLoading,
    debounce,
    getCurrentTheme,
    setTheme
};

/**
 * Search Autocomplete Functionality
 */
function initializeSearchAutocomplete() {
    const searchInput = document.getElementById('search-input');
    const suggestionsContainer = document.getElementById('search-suggestions');
    
    if (!searchInput || !suggestionsContainer) return;
    
    let currentRequest = null;
    let selectedIndex = -1;
    let suggestions = [];
    
    // Debounced search function
    const debouncedSearch = debounce(performSearch, 300);
    
    // Input event listener
    searchInput.addEventListener('input', function(e) {
        const query = e.target.value.trim();
        
        if (query.length === 0) {
            hideSuggestions();
            return;
        }
        
        if (query.length >= 1) {
            debouncedSearch(query);
        }
    });
    
    // Keyboard navigation
    searchInput.addEventListener('keydown', function(e) {
        if (!suggestionsContainer.classList.contains('show')) return;
        
        switch(e.key) {
            case 'ArrowDown':
                e.preventDefault();
                selectedIndex = Math.min(selectedIndex + 1, suggestions.length - 1);
                updateSelection();
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                selectedIndex = Math.max(selectedIndex - 1, -1);
                updateSelection();
                break;
                
            case 'Enter':
                e.preventDefault();
                if (selectedIndex >= 0 && suggestions[selectedIndex]) {
                    selectSuggestion(suggestions[selectedIndex]);
                } else {
                    // Submit the form with current input value
                    searchInput.closest('form').submit();
                }
                break;
                
            case 'Escape':
                hideSuggestions();
                searchInput.blur();
                break;
        }
    });
    
    // Click outside to close
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !suggestionsContainer.contains(e.target)) {
            hideSuggestions();
        }
    });
    
    // Focus event to show suggestions if there's a query
    searchInput.addEventListener('focus', function() {
        const query = this.value.trim();
        if (query.length >= 1 && suggestions.length > 0) {
            showSuggestions();
        }
    });
    
    /**
     * Perform search API call
     */
    function performSearch(query) {
        // Cancel previous request
        if (currentRequest) {
            currentRequest.abort();
        }
        
        // Show loading state
        showLoadingState();
        
        // Create new request
        const controller = new AbortController();
        currentRequest = controller;
        
        fetch(`/api/products/autocomplete?q=${encodeURIComponent(query)}&limit=8`, {
            signal: controller.signal
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            suggestions = data.suggestions || [];
            displaySuggestions(suggestions, query);
        })
        .catch(error => {
            if (error.name !== 'AbortError') {
                console.error('Search error:', error);
                showErrorState();
            }
        })
        .finally(() => {
            currentRequest = null;
        });
    }
    
    /**
     * Display search suggestions
     */
    function displaySuggestions(products, query) {
        selectedIndex = -1;
        
        if (products.length === 0) {
            showNoResults(query);
            return;
        }
        
        const html = products.map((product, index) => {
            const imageUrl = product.image_url ? 
                `/static/images/${product.image_url}` : 
                '/static/images/placeholder.jpg';
            
            return `
                <div class="search-suggestion-item" data-index="${index}" data-product-id="${product.id}">
                    <div class="suggestion-image">
                        <img src="${imageUrl}" alt="${product.name}" 
                             onerror="this.style.display='none'; this.parentNode.innerHTML='📦';">
                    </div>
                    <div class="suggestion-content">
                        <div class="suggestion-name">${highlightMatch(product.name, query)}</div>
                        <div class="suggestion-category">${product.category_name || 'Uncategorized'}</div>
                    </div>
                    <div class="suggestion-price">$${parseFloat(product.price).toFixed(2)}</div>
                </div>
            `;
        }).join('');
        
        suggestionsContainer.innerHTML = html;
        showSuggestions();
        
        // Add click listeners to suggestion items
        suggestionsContainer.querySelectorAll('.search-suggestion-item').forEach(item => {
            item.addEventListener('click', function() {
                const productId = this.getAttribute('data-product-id');
                const product = products.find(p => p.id == productId);
                if (product) {
                    selectSuggestion(product);
                }
            });
        });
    }
    
    /**
     * Show loading state
     */
    function showLoadingState() {
        suggestionsContainer.innerHTML = `
            <div class="search-loading">
                <i class="fas fa-spinner fa-spin"></i> Searching...
            </div>
        `;
        showSuggestions();
    }
    
    /**
     * Show error state
     */
    function showErrorState() {
        suggestionsContainer.innerHTML = `
            <div class="search-no-results">
                <i class="fas fa-exclamation-triangle"></i> Search failed. Please try again.
            </div>
        `;
        showSuggestions();
    }
    
    /**
     * Show no results state
     */
    function showNoResults(query) {
        suggestionsContainer.innerHTML = `
            <div class="search-no-results">
                No products found for "${query}"
            </div>
        `;
        showSuggestions();
    }
    
    /**
     * Show suggestions container
     */
    function showSuggestions() {
        suggestionsContainer.classList.add('show');
    }
    
    /**
     * Hide suggestions container
     */
    function hideSuggestions() {
        suggestionsContainer.classList.remove('show');
        selectedIndex = -1;
    }
    
    /**
     * Update visual selection
     */
    function updateSelection() {
        const items = suggestionsContainer.querySelectorAll('.search-suggestion-item');
        
        items.forEach((item, index) => {
            if (index === selectedIndex) {
                item.classList.add('highlighted');
            } else {
                item.classList.remove('highlighted');
            }
        });
    }
    
    /**
     * Select a suggestion
     */
    function selectSuggestion(product) {
        // Navigate to product detail page
        window.location.href = `/product/${product.id}`;
    }
    
    /**
     * Highlight matching text
     */
    function highlightMatch(text, query) {
        if (!query) return text;
        
        const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
        return text.replace(regex, '<strong>$1</strong>');
    }
    
    /**
     * Escape regex special characters
     */
    function escapeRegex(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }
}