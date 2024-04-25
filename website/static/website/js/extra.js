
document.addEventListener("DOMContentLoaded", function() {
    // Select all the read more links and additional text elements
    var readMoreLinks = document.querySelectorAll('.read-more-link');
    var additionalTexts = document.querySelectorAll('.additional-text');

    // Add click event listener to each read more link
    readMoreLinks.forEach(function(link, index) {
        link.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent the default link behavior
            if (additionalTexts[index].style.display === 'none' || additionalTexts[index].style.display === '') {
                additionalTexts[index].style.display = 'block'; // Show additional text
                link.textContent = 'Read Less'; // Change link text
            } else {
                additionalTexts[index].style.display = 'none'; // Hide additional text
                link.textContent = 'Read More'; // Change link text
            }
        });
    });
});



document.addEventListener("DOMContentLoaded", function() {
    var navLinks = document.querySelectorAll(".navbar-nav .nav-link");

    navLinks.forEach(function(link) {
      link.addEventListener("click", function() {
        // Remove active class from all links
        navLinks.forEach(function(link) {
          link.classList.remove("active");
        });

        // Add active class to clicked link
        this.classList.add("active");
      });
    });
  });