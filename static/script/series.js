document.addEventListener('DOMContentLoaded', function() {
    const genreButtons = document.querySelectorAll('.genre-button');
    const selectedGenresInput = document.getElementById('selected_genres');
    const moviesGrid = document.querySelector('.movies-grid');
    let selectedGenres = [];

    // Inicializar los botones de género
    initializeGenreButtons();

    genreButtons.forEach(button => {
        button.addEventListener('click', function() {
            const genreId = this.dataset.id;

            // Verificar si el género ya está seleccionado
            if (selectedGenres.includes(genreId)) {
                selectedGenres = selectedGenres.filter(id => id !== genreId); // Remover género
                this.classList.remove('active'); // Quitar clase activa
            } else {
                selectedGenres.push(genreId); // Agregar género
                this.classList.add('active'); // Agregar clase activa
            }

            // Actualizar el input oculto
            selectedGenresInput.value = selectedGenres.join(',');

            // Reiniciar paginación y cargar la primera página
            loadSeries(1);
        });
    });
});
// Función para cargar series
function loadSeries(page) {
    const categoria = '{{ categoria }}'; // Reemplaza con la categoría actual
    const selectedGenresStr = encodeURIComponent(selectedGenres.join(',')); // Codificar géneros

    fetch(`/series/${categoria}?selected_genres=${selectedGenresStr}&page=${page}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(html => {
            moviesGrid.innerHTML = html; // Actualizar la cuadrícula de películas
            initializeGenreButtons(); // Re-aplicar los géneros seleccionados
        })
        .catch(error => {
            console.error("Error en la solicitud AJAX:", error);
        });
}

// Manejar clics en botones de paginación
const paginationButtons = document.querySelectorAll('.pagination-button');
paginationButtons.forEach(button => {
    button.addEventListener('click', function() {
        const page = this.dataset.page; // Obtener número de página
        loadSeries(page); // Cargar series de la página correspondiente
    });
});

// Función para inicializar botones de género
function initializeGenreButtons() {
    const selectedGenres = selectedGenresInput.value.split(',');
    selectedGenres.forEach(genreId => {
        const button = document.querySelector(`.genre-button[data-id="${genreId}"]`);
        if (button) {
            button.classList.add('active'); // Activar el botón correspondiente
        }
    });
}
