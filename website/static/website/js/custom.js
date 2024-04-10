// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();


// client section owl carousel
$(".client_owl-carousel").owlCarousel({
    loop: true,
    margin: 20,
    dots: false,
    nav: true,
    navText: [],
    autoplay: true,
    autoplayHoverPause: true,
    navText: [
        '<i class="fa fa-angle-left" aria-hidden="true"></i>',
        '<i class="fa fa-angle-right" aria-hidden="true"></i>'
    ],
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 2
        },
        1000: {
            items: 2
        }
    }
});



/** google_map js **/
function myMap() {
    var mapProp = {
        center: new google.maps.LatLng(40.712775, -74.005973),
        zoom: 18,
    };
    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
}
document.addEventListener("DOMContentLoaded", function() {
    // Select the read more link and additional text
    var readMoreLink = document.querySelector('.read-more-link');
    var additionalText = document.querySelector('.additional-text');

    // Add click event listener to the read more link
    readMoreLink.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default link behavior
        if (additionalText.style.display === 'none') {
            additionalText.style.display = 'block'; // Show additional text
            readMoreLink.textContent = 'Read Less'; // Change link text
        } else {
            additionalText.style.display = 'none'; // Hide additional text
            readMoreLink.textContent = 'Read More'; // Change link text
        }
    });
});