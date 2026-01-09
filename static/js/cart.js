/**
 * Shopping Cart JavaScript functionality
 * Handles add to cart, update quantity, remove items with throttling
 */

// Track ongoing requests to prevent duplicates
const ongoingRequests = new Map();

// Global click throttling
let lastClickTime = 0;
const CLICK_THROTTLE_MS = 300; // Minimum time between clicks

document.addEventListener('DOMContentLoaded', function() {
    initializeCartFunctionality();
});

/**
 * Initialize cart functionality
 */
function initializeCartFunctionality() {
    console.log('Initializing cart functionality...');
    
    initializeAddToCartButtons();
    initializeCartUpdateButtons();
    initializeCartRemoveButtons();
    initializeQuantityInputs();
    
    // Debug: Log found elements
    const updateButtons = document.querySelectorAll('.update-cart-btn');
    const quantityInputs = document.querySelectorAll('.quantity-input');
    const removeButtons = document.querySelectorAll('.remove-cart-btn');
    
    console.log(`Found ${updateButtons.length} update buttons`);
    console.log(`Found ${quantityInputs.length} quantity inputs`);
    console.log(`Found ${removeButtons.length} remove buttons`);
    
    // Add click event listeners to all buttons for debugging
    updateButtons.forEach((button, index) => {
        console.log(`Update button ${index}:`, {
            productId: button.getAttribute('data-product-id'),
            action: button.getAttribute('data-action'),
            disabled: button.disabled
        });
    });
}

/**
 * Initialize Add to Cart buttons
 */
function initializeAddToCartButtons() {
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    
    console.log(`Found ${addToCartButtons.length} add to cart buttons`);
    
    addToCartButtons.forEach((button, index) => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            
            // Try to get quantity from quantity selector input first
            let quantity = 1;
            const quantityInput = document.querySelector('.quantity-input');
            if (quantityInput) {
                quantity = parseInt(quantityInput.value) || 1;
                console.log(`Button ${index}: Found quantity selector with value: ${quantity}`);
            } else {
                // Fallback to data-quantity attribute
                quantity = parseInt(this.getAttribute('data-quantity')) || 1;
                console.log(`Button ${index}: Using fallback quantity: ${quantity}`);
            }
            
            console.log(`Button ${index}: Adding to cart - Product ${productId}, Quantity ${quantity}`);
            addToCart(productId, quantity, this);
        });
        
        console.log(`Button ${index}: Product ID ${button.getAttribute('data-product-id')}`);
    });
}

/**
 * Initialize cart update buttons with throttling
 */
function initializeCartUpdateButtons() {
    const updateButtons = document.querySelectorAll('.update-cart-btn');
    
    updateButtons.forEach(button => {
        // Remove any existing event listeners by cloning the button
        const newButton = button.cloneNode(true);
        button.parentNode.replaceChild(newButton, button);
    });
    
    // Add event listeners to the fresh buttons
    const freshButtons = document.querySelectorAll('.update-cart-btn');
    freshButtons.forEach(button => {
        button.addEventListener('click', handleCartUpdate, { once: false });
    });
    
    console.log(`Initialized ${freshButtons.length} cart update buttons`);
}

/**
 * Handle cart update button clicks with strict single-click enforcement
 */
function handleCartUpdate(event) {
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();
    
    // Global throttling check
    const now = Date.now();
    if (now - lastClickTime < CLICK_THROTTLE_MS) {
        console.log('Click throttled - too fast');
        return false;
    }
    lastClickTime = now;
    
    const button = event.target;
    const productId = button.getAttribute('data-product-id');
    const action = button.getAttribute('data-action');
    
    // Check if button is already processing
    if (button.hasAttribute('data-processing')) {
        console.log('Button click ignored - already processing');
        return false;
    }
    
    // Mark button as processing
    button.setAttribute('data-processing', 'true');
    button.disabled = true;
    
    // Visual feedback
    const originalBg = button.style.backgroundColor;
    const originalColor = button.style.color;
    button.style.backgroundColor = '#007bff';
    button.style.color = 'white';
    
    const quantityInput = document.querySelector(`input[data-product-id="${productId}"]`);
    
    if (!quantityInput) {
        console.error('Quantity input not found for product:', productId);
        resetButton();
        return false;
    }
    
    let currentQuantity = parseInt(quantityInput.value) || 1;
    let newQuantity = currentQuantity;
    
    if (action === 'increase') {
        const maxStock = parseInt(quantityInput.getAttribute('max')) || 999;
        if (currentQuantity < maxStock) {
            newQuantity = currentQuantity + 1;
        } else {
            ECommerce.showNotification('Maximum quantity reached', 'warning');
            resetButton();
            return false;
        }
    } else if (action === 'decrease') {
        if (currentQuantity > 0) {
            newQuantity = currentQuantity - 1;
            
            // Show confirmation for removal when quantity becomes 0
            if (newQuantity === 0) {
                const productName = quantityInput.closest('.cart-item').querySelector('.item-details h3')?.textContent || 'this item';
                if (!confirm(`Remove ${productName} from your cart?`)) {
                    resetButton();
                    return false;
                }
            }
        } else {
            // Already at 0, can't decrease further
            ECommerce.showNotification('Item quantity is already 0', 'warning');
            resetButton();
            return false;
        }
    }
    
    // Update the input value immediately for better UX
    quantityInput.value = newQuantity;
    
    console.log(`Updating quantity from ${currentQuantity} to ${newQuantity} for product ${productId}`);
    
    // Call the update function with callback to reset button
    updateCartItem(productId, newQuantity, quantityInput, resetButton);
    
    function resetButton() {
        setTimeout(() => {
            button.style.backgroundColor = originalBg;
            button.style.color = originalColor;
            button.disabled = false;
            button.removeAttribute('data-processing');
        }, 500); // Longer delay to prevent rapid clicking
    }
    
    return false;
}

/**
 * Initialize cart remove buttons
 */
function initializeCartRemoveButtons() {
    const removeButtons = document.querySelectorAll('.remove-cart-btn');
    
    removeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            
            if (confirm('Are you sure you want to remove this item from your cart?')) {
                removeFromCart(productId, this);
            }
        });
    });
}

/**
 * Initialize quantity inputs with debouncing
 */
function initializeQuantityInputs() {
    const quantityInputs = document.querySelectorAll('.quantity-input');
    
    quantityInputs.forEach(input => {
        // Store original value
        input.setAttribute('data-original-value', input.value);
        
        // Remove existing listeners
        input.removeEventListener('change', handleQuantityChange);
        input.removeEventListener('input', handleQuantityInput);
        
        // Add change event (when user finishes editing)
        input.addEventListener('change', handleQuantityChange);
        
        // Add input event for real-time validation
        input.addEventListener('input', handleQuantityInput);
    });
}

/**
 * Handle quantity input changes
 */
function handleQuantityChange(event) {
    const input = event.target;
    const productId = input.getAttribute('data-product-id');
    const quantity = parseInt(input.value);
    const minQuantity = 0; // Allow 0 to remove items
    const maxQuantity = parseInt(input.getAttribute('max')) || 999;
    
    // Handle empty or invalid input
    if (isNaN(quantity)) {
        input.value = input.getAttribute('data-original-value') || 1;
        return;
    }
    
    // Validate quantity
    let validQuantity = quantity;
    if (quantity < minQuantity) {
        validQuantity = minQuantity;
        ECommerce.showNotification(`Minimum quantity is ${minQuantity}`, 'warning');
    } else if (quantity > maxQuantity) {
        validQuantity = maxQuantity;
        ECommerce.showNotification(`Maximum quantity is ${maxQuantity}`, 'warning');
    }
    
    // Show confirmation for removal when quantity becomes 0
    if (validQuantity === 0) {
        const productName = input.closest('.cart-item').querySelector('.item-details h3')?.textContent || 'this item';
        if (!confirm(`Remove ${productName} from your cart?`)) {
            input.value = input.getAttribute('data-original-value') || 1;
            return;
        }
    }
    
    // Update input if needed
    if (validQuantity !== quantity) {
        input.value = validQuantity;
    }
    
    // Update cart if quantity changed
    const originalValue = parseInt(input.getAttribute('data-original-value')) || 1;
    if (validQuantity !== originalValue) {
        updateCartItem(productId, validQuantity, input);
    }
}

/**
 * Handle quantity input typing (real-time validation)
 */
function handleQuantityInput(event) {
    const input = event.target;
    const value = input.value;
    
    // Allow empty input while typing
    if (value === '') return;
    
    // Ensure only numbers
    if (!/^\d+$/.test(value)) {
        input.value = input.getAttribute('data-original-value') || '1';
        return;
    }
    
    const quantity = parseInt(value);
    const maxQuantity = parseInt(input.getAttribute('max')) || 999;
    
    // Visual feedback for max quantity
    if (quantity > maxQuantity) {
        input.style.borderColor = '#dc3545';
        input.style.backgroundColor = '#fff5f5';
    } else {
        input.style.borderColor = '';
        input.style.backgroundColor = '';
    }
}

/**
 * Add product to cart with duplicate request prevention
 */
function addToCart(productId, quantity = 1, buttonElement = null) {
    const requestKey = `add-${productId}`;
    
    // Prevent duplicate requests
    if (ongoingRequests.has(requestKey)) {
        console.log('Duplicate add to cart request prevented for product:', productId);
        return;
    }
    
    console.log(`Adding to cart: Product ${productId}, Quantity ${quantity}`);
    
    if (buttonElement) {
        buttonElement.disabled = true;
        buttonElement.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';
    }
    
    const data = {
        product_id: parseInt(productId),
        quantity: parseInt(quantity)
    };
    
    // Mark request as ongoing
    ongoingRequests.set(requestKey, true);
    
    ECommerce.makeAjaxRequest('/api/cart/add', {
        method: 'POST',
        body: JSON.stringify(data)
    })
    .then(response => {
        console.log('Add to cart response:', response);
        
        if (response.success) {
            ECommerce.showNotification(response.message, 'success');
            ECommerce.updateCartCount(response.cart_count);
            console.log(`Cart updated: ${response.cart_count} total items`);
        } else {
            ECommerce.showNotification(response.message, 'error');
            console.error('Add to cart failed:', response.message);
        }
    })
    .catch(error => {
        console.error('Add to cart error:', error);
        ECommerce.showNotification('Failed to add item to cart', 'error');
    })
    .finally(() => {
        // Remove from ongoing requests
        ongoingRequests.delete(requestKey);
        
        if (buttonElement) {
            buttonElement.disabled = false;
            buttonElement.innerHTML = 'Add to Cart';
        }
    });
}

/**
 * Update cart item quantity with duplicate request prevention
 */
function updateCartItem(productId, quantity, inputElement = null, callback = null) {
    const requestKey = `update-${productId}`;
    
    // Prevent duplicate requests
    if (ongoingRequests.has(requestKey)) {
        console.log('Request already in progress for product:', productId);
        if (callback) callback();
        return;
    }
    
    const data = {
        product_id: parseInt(productId),
        quantity: quantity
    };
    
    // Mark request as ongoing
    ongoingRequests.set(requestKey, true);
    
    // Store original value for rollback
    if (inputElement) {
        inputElement.setAttribute('data-original-value', inputElement.value);
    }
    
    ECommerce.makeAjaxRequest('/api/cart/update', {
        method: 'POST',
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.success) {
            // Only show notification for manual updates, not automatic ones
            if (inputElement && document.activeElement === inputElement) {
                ECommerce.showNotification(response.message, 'success');
            }
            ECommerce.updateCartCount(response.cart_count);
            
            // Update cart totals if on cart page
            updateCartTotals();
            
            // Remove row if quantity is 0
            if (quantity === 0 && inputElement) {
                const cartRow = inputElement.closest('.cart-item');
                if (cartRow) {
                    cartRow.style.opacity = '0';
                    setTimeout(() => {
                        cartRow.remove();
                        updateCartTotals();
                    }, 300);
                }
            }
        } else {
            ECommerce.showNotification(response.message, 'error');
            // Reset input value on error
            if (inputElement) {
                inputElement.value = inputElement.getAttribute('data-original-value') || 1;
            }
        }
    })
    .catch(error => {
        ECommerce.showNotification('Failed to update cart', 'error');
        if (inputElement) {
            inputElement.value = inputElement.getAttribute('data-original-value') || 1;
        }
    })
    .finally(() => {
        // Remove from ongoing requests
        ongoingRequests.delete(requestKey);
        if (callback) callback();
    });
}

/**
 * Remove item from cart with duplicate request prevention
 */
function removeFromCart(productId, buttonElement = null) {
    const requestKey = `remove-${productId}`;
    
    // Prevent duplicate requests
    if (ongoingRequests.has(requestKey)) {
        return;
    }
    
    if (buttonElement) {
        buttonElement.disabled = true;
        buttonElement.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    }
    
    const data = {
        product_id: parseInt(productId)
    };
    
    // Mark request as ongoing
    ongoingRequests.set(requestKey, true);
    
    ECommerce.makeAjaxRequest('/api/cart/remove', {
        method: 'POST',
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.success) {
            ECommerce.showNotification(response.message, 'success');
            ECommerce.updateCartCount(response.cart_count);
            
            // Remove cart item row
            if (buttonElement) {
                const cartRow = buttonElement.closest('.cart-item');
                if (cartRow) {
                    cartRow.style.opacity = '0';
                    setTimeout(() => {
                        cartRow.remove();
                        updateCartTotals();
                        
                        // Check if cart is empty
                        const remainingItems = document.querySelectorAll('.cart-item');
                        if (remainingItems.length === 0) {
                            showEmptyCartMessage();
                        }
                    }, 300);
                }
            }
        } else {
            ECommerce.showNotification(response.message, 'error');
        }
    })
    .catch(error => {
        ECommerce.showNotification('Failed to remove item', 'error');
    })
    .finally(() => {
        // Remove from ongoing requests
        ongoingRequests.delete(requestKey);
        
        if (buttonElement) {
            buttonElement.disabled = false;
            buttonElement.innerHTML = '<i class="fas fa-trash"></i>';
        }
    });
}

/**
 * Update cart totals on cart page
 */
function updateCartTotals() {
    const cartItems = document.querySelectorAll('.cart-item');
    let subtotal = 0;
    
    cartItems.forEach(item => {
        const priceElement = item.querySelector('.item-price');
        const quantityElement = item.querySelector('.quantity-input');
        
        if (priceElement && quantityElement) {
            const price = parseFloat(priceElement.getAttribute('data-price'));
            const quantity = parseInt(quantityElement.value);
            const itemTotal = price * quantity;
            
            // Update item subtotal display
            const subtotalElement = item.querySelector('.item-subtotal');
            if (subtotalElement) {
                subtotalElement.textContent = ECommerce.formatCurrency(itemTotal);
            }
            
            subtotal += itemTotal;
        }
    });
    
    // Update totals
    const subtotalElement = document.getElementById('cart-subtotal');
    const taxElement = document.getElementById('cart-tax');
    const shippingElement = document.getElementById('cart-shipping');
    const totalElement = document.getElementById('cart-total');
    
    if (subtotalElement) {
        subtotalElement.textContent = ECommerce.formatCurrency(subtotal);
    }
    
    const tax = subtotal * 0.08; // 8% tax
    const shipping = subtotal > 0 ? 10.00 : 0; // $10 shipping
    const total = subtotal + tax + shipping;
    
    if (taxElement) {
        taxElement.textContent = ECommerce.formatCurrency(tax);
    }
    
    if (shippingElement) {
        shippingElement.textContent = ECommerce.formatCurrency(shipping);
    }
    
    if (totalElement) {
        totalElement.textContent = ECommerce.formatCurrency(total);
    }
}

/**
 * Show empty cart message
 */
function showEmptyCartMessage() {
    const cartContainer = document.querySelector('.cart-container');
    if (cartContainer) {
        cartContainer.innerHTML = `
            <div class="empty-cart">
                <div class="empty-cart-icon">
                    <i class="fas fa-shopping-cart"></i>
                </div>
                <h2>Your cart is empty</h2>
                <p>Looks like you haven't added any items to your cart yet.</p>
                <a href="/products" class="btn btn-primary">Continue Shopping</a>
            </div>
        `;
    }
}

/**
 * Show loading state for cart operations
 */
function showCartLoading(element, message = 'Processing...') {
    if (element) {
        element.classList.add('loading');
        const originalContent = element.innerHTML;
        element.setAttribute('data-original-content', originalContent);
        element.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${message}`;
    }
}

/**
 * Hide loading state for cart operations
 */
function hideCartLoading(element) {
    if (element && element.classList.contains('loading')) {
        element.classList.remove('loading');
        const originalContent = element.getAttribute('data-original-content');
        if (originalContent) {
            element.innerHTML = originalContent;
            element.removeAttribute('data-original-content');
        }
    }
}

/**
 * Initialize product quantity selector
 */
function initializeProductQuantitySelector() {
    const quantityContainer = document.querySelector('.quantity-selector');
    
    if (quantityContainer) {
        const decreaseBtn = quantityContainer.querySelector('.quantity-decrease');
        const increaseBtn = quantityContainer.querySelector('.quantity-increase');
        const quantityInput = quantityContainer.querySelector('.quantity-input');
        
        if (decreaseBtn && increaseBtn && quantityInput) {
            decreaseBtn.addEventListener('click', ECommerce.debounce(function() {
                let currentValue = parseInt(quantityInput.value);
                if (currentValue > 1) {
                    quantityInput.value = currentValue - 1;
                    quantityInput.dispatchEvent(new Event('change'));
                }
            }, 200));
            
            increaseBtn.addEventListener('click', ECommerce.debounce(function() {
                let currentValue = parseInt(quantityInput.value);
                const maxStock = parseInt(quantityInput.getAttribute('max'));
                
                if (!maxStock || currentValue < maxStock) {
                    quantityInput.value = currentValue + 1;
                    quantityInput.dispatchEvent(new Event('change'));
                } else {
                    ECommerce.showNotification(`Only ${maxStock} items available in stock`, 'warning');
                }
            }, 200));
            
            quantityInput.addEventListener('change', function() {
                let value = parseInt(this.value);
                const maxStock = parseInt(this.getAttribute('max'));
                
                if (isNaN(value) || value < 1) {
                    this.value = 1;
                } else if (maxStock && value > maxStock) {
                    this.value = maxStock;
                    ECommerce.showNotification(`Only ${maxStock} items available in stock`, 'warning');
                }
            });
        }
    }
}

/**
 * Get cart count from server
 */
function refreshCartCount() {
    ECommerce.makeAjaxRequest('/api/cart/count')
        .then(response => {
            ECommerce.updateCartCount(response.cart_count);
        })
        .catch(error => {
            console.error('Failed to refresh cart count:', error);
        });
}

// Initialize product quantity selector when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeProductQuantitySelector();
});

// Export functions for use in other files
window.Cart = {
    addToCart,
    updateCartItem,
    removeFromCart,
    updateCartTotals,
    refreshCartCount,
    showCartLoading,
    hideCartLoading,
    // Debug function
    testButtons: function() {
        console.log('Testing cart buttons...');
        const updateButtons = document.querySelectorAll('.update-cart-btn');
        updateButtons.forEach((button, index) => {
            console.log(`Button ${index}:`, button);
            button.style.border = '2px solid red';
            setTimeout(() => {
                button.style.border = '';
            }, 2000);
        });
    }
};