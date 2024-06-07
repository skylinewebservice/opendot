document.addEventListener('DOMContentLoaded', function() {
    const cartItemsContainer = document.querySelector('.cart-items');
    const itemsPriceElement = document.getElementById('items-price');
    const estimatedTaxElement = document.getElementById('estimated-tax');
    const totalPriceElement = document.getElementById('total-price');
    const cartCount = document.querySelector('.cart-count');
    const clearCartButton = document.querySelector('.clear-cart-button');
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    let itemsPrice = 0;
    let estimatedTax = 0;
    let totalPrice = 0;

    function updateCartCount() {
        if (cartCount) {  // Ensure cartCount element exists
            cartCount.textContent = cart.length;
        }
    }

    function displayCartItems() {
        cartItemsContainer.innerHTML = ''; // Clear any existing content
        itemsPrice = 0; // Reset items price
        cart.forEach((item, index) => {
            const cartItem = document.createElement('div');
            cartItem.classList.add('cart-item');
            cartItem.innerHTML = `
                <div class="cart-item-details">
                    <div class="cart-item-image">
                        <img src="${item.image}" alt="${item.name}">
                    </div>
                    <div class="cart-item-info">
                        <span>${item.name}</span>
                        <span>Quantity: 1</span> <!-- Assuming quantity is 1 for simplicity -->
                        <span>$${item.price.toFixed(2)}</span>
                        <button class="remove-item" data-index="${index}">Remove</button>
                    </div>
                </div>
            `;
            cartItemsContainer.appendChild(cartItem);
            itemsPrice += item.price; // Adding each item's price to the items price
        });
        estimatedTax = itemsPrice * 0.1; // Assuming a 10% tax rate
        totalPrice = itemsPrice + estimatedTax;

        itemsPriceElement.textContent = itemsPrice.toFixed(2);
        estimatedTaxElement.textContent = estimatedTax.toFixed(2);
        totalPriceElement.textContent = totalPrice.toFixed(2);
    }

    displayCartItems();
    updateCartCount();

    document.querySelector('.checkout-button').addEventListener('click', function() {
        alert('Proceeding to payment (not implemented)');
        // Implement payment process here
    });

    clearCartButton.addEventListener('click', function() {
        cart = [];
        localStorage.setItem('cart', JSON.stringify(cart));
        displayCartItems();
        updateCartCount();
    });

    // Event delegation to handle remove item button click
    cartItemsContainer.addEventListener('click', function(event) {
        if (event.target.classList.contains('remove-item')) {
            const index = event.target.dataset.index;
            cart.splice(index, 1); // Remove item from cart array
            localStorage.setItem('cart', JSON.stringify(cart)); // Update localStorage
            displayCartItems(); // Update cart display
            updateCartCount(); // Update cart count
        }
    });
});
