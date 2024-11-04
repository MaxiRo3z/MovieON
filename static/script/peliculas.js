document.addEventListener('DOMContentLoaded', function () {
    initializeGenreButtons();  // Activar los géneros seleccionados al cargar la página
});

function initializeGenreButtons() {
    const selectedGenres = document.getElementById('selected_genres').value.split(',');
    selectedGenres.forEach(genreId => {
        const button = document.querySelector(`.genre-button[data-id="${genreId}"]`);
        if (button) {
            button.classList.add('active'); // Activar el botón correspondiente
        }
    });
}

function toggleGenre(button) {
    button.classList.toggle('active');
    updateGenres();
}

function updateGenres(page = 1) {
    const selectedGenres = Array.from(document.querySelectorAll('.genre-button.active'))
        .map(button => button.getAttribute('data-id'));

    document.getElementById('selected_genres').value = selectedGenres.join(',');

    fetch(`/peliculas/{{ categoria }}?selected_genres=${selectedGenres.join(',')}&page=${page}`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(html => {
        document.querySelector('.movies-grid').innerHTML = html;  // Actualiza solo la cuadrícula
        initializeGenreButtons(); // Re-aplica los géneros seleccionados en la nueva página
    })
    .catch(error => console.log("Error en la solicitud AJAX:", error));
}

function submitFilter() {
    updateGenres(1);
}