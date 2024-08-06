document.addEventListener('DOMContentLoaded', function() {
    // Carousel functionality
    const carousel = document.querySelector('.carousel');
    let currentIndex = 0;
    const images = carousel.querySelectorAll('img');
    const totalImages = images.length;
    const previews = document.querySelectorAll('.preview img');

    function showImage(index) {
        images.forEach((img, i) => {
            img.classList.toggle('active', i === index);
            previews[i].classList.toggle('active', i === index);
        });
    }

    function nextImage() {
        currentIndex = (currentIndex + 1) % totalImages;
        showImage(currentIndex);
    }

    function prevImage() {
        currentIndex = (currentIndex - 1 + totalImages) % totalImages;
        showImage(currentIndex);
    }

    showImage(currentIndex);

    const prevButton = carousel.querySelector('.prev');
    const nextButton = carousel.querySelector('.next');

    prevButton.addEventListener('click', prevImage);
    nextButton.addEventListener('click', nextImage);

    previews.forEach((preview, index) => {
        preview.addEventListener('click', function() {
            currentIndex = index;
            showImage(index);
        });
    });

    // Fullscreen image modal
    const modal = document.getElementById("myModal");
    const modalImg = document.getElementById("img01");
    const closeSpan = modal.querySelector('.close');

    images.forEach((img) => {
        img.addEventListener('click', function() {
            modal.style.display = "block";
            modalImg.src = img.src;
        });
    });

    closeSpan.onclick = function() {
        modal.style.display = "none";
    };

    // Price detail modal
    const openPriceDetailModalButton = document.getElementById('openPriceDetailModal');
    const priceDetailModal = document.getElementById('priceDetailModal');
    const closeModalButton = priceDetailModal.querySelector('.icon-btn.lightbox-dialog__close');

    openPriceDetailModalButton.addEventListener('click', function(event) {
        event.preventDefault();
        priceDetailModal.style.display = 'block';
    });

    closeModalButton.addEventListener('click', function() {
        priceDetailModal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target === priceDetailModal) {
            priceDetailModal.style.display = 'none';
        }
    });

});