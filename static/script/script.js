document.addEventListener("DOMContentLoaded", function() {
    const API_KEY = 'cc0bbbd7774ce2853272ceeb3db7db56'; // Reemplaza con tu clave de API real
    const API_URL = `https://api.themoviedb.org/3/movie/upcoming?api_key=${API_KEY}&language=es-ES&page=1`; // Endpoint para obtener próximas películas

    fetch(API_URL)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const movies = data.results;
            const carouselInner = document.getElementById('carousel-inner');
            let slides = '';

            movies.forEach((movie) => {
                const posterPath = `https://image.tmdb.org/t/p/w500${movie.poster_path}`;
                slides += `
                    <div class="carousel-item">
                        <img src="${posterPath}" alt="${movie.title}">
                    </div>
                `;
            });

            carouselInner.innerHTML = slides;
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });

    let slideIndex = 0;

    window.plusSlides = function(n) {
        showSlides(slideIndex += n);
    }

    function showSlides(n) {
        const slides = document.getElementsByClassName("carousel-item");
        const totalSlides = slides.length;
        const containerWidth = document.querySelector('.carousel-container').offsetWidth;
        const slideWidth = slides[0].offsetWidth;

        if (n >= totalSlides) { slideIndex = 0 }
        if (n < 0) { slideIndex = totalSlides - Math.floor(containerWidth / slideWidth) }

        const offset = -(slideWidth * slideIndex);
        document.querySelector('.carousel-inner').style.transform = `translateX(${offset}px)`;
    }
});

