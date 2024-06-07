document.addEventListener('DOMContentLoaded', function() {
    const cartCount = document.querySelector('.cart-count');
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    function updateCartCount() {
        cartCount.textContent = cart.length;
    }

    function addToCart(product) {
        cart.push(product);
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartCount();
    }

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const product = this.getAttribute('data-product');
            addToCart(product);
            alert(`${product} added to cart`);
        });
    });

    updateCartCount();

    const carousels = document.querySelectorAll('.carousel');
    carousels.forEach(carousel => {
        let images = carousel.querySelectorAll('img');
        let currentIndex = 0;

        function showImage(index) {
            images.forEach((img, i) => {
                img.classList.toggle('active', i === index);
            });
        }

        carousel.querySelector('.prev').addEventListener('click', function() {
            currentIndex = (currentIndex === 0) ? images.length - 1 : currentIndex - 1;
            showImage(currentIndex);
        });

        carousel.querySelector('.next').addEventListener('click', function() {
            currentIndex = (currentIndex === images.length - 1) ? 0 : currentIndex + 1;
            showImage(currentIndex);
        });

        showImage(currentIndex);
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const cartCount = document.querySelector('.cart-count');
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    function updateCartCount() {
        cartCount.textContent = cart.length;
    }

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const product = {
                name: this.dataset.product,
                price: parseFloat(this.dataset.price),
                image: this.dataset.image
            };
            cart.push(product);
            localStorage.setItem('cart', JSON.stringify(cart));
            updateCartCount();
        });
    });

    updateCartCount();
});