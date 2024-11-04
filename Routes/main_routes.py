from flask import render_template, request, url_for
import math
from services.api_service import *
from . import main_bp
from cache_config import cache  # Importa cache aquí

GENEROS_PELICULAS= {
    "28": "Acción",
    "12": "Aventura",
    "16": "Animación",
    "35": "Comedia",
    "80": "Crimen",
    "99": "Documental",
    "18": "Drama",
    "10751": "Familia",
    "14": "Fantasía",
    "36": "Historia",
    "27": "Terror",
    "10402": "Música",
    "9648": "Misterio",
    "10770": "Película de TV",
    "10749": "Romance",
    "878": "Ciencia ficción",
    "53": "Suspense",
    "10752": "Bélica",
    "37": "Western",
    # Agrega más géneros aquí si es necesario
}


GENEROS_SERIES= {
    "28": "Acción",
    "12": "Aventura",
    "16": "Animación",
    "35": "Comedia",
    "80": "Crimen",
    "99": "Documental",
    "18": "Drama",
    "10751": "Familia",
    "14": "Fantasía",
    "36": "Historia",
    "27": "Terror",
    "10402": "Música",
    "9648": "Misterio",
    "10770": "Película de TV",
    "10749": "Romance",
    "878": "Ciencia ficción",
    "53": "Suspense",
    "10752": "Bélica",
    "37": "Western",
    "10759": "Acción y Aventura",
    "10765": "Ciencia ficción y Fantasía",
    "10766": "Telenovela",
    "10767": "Reality",
    "10768": "Guerra",
}

@main_bp.route("/")
def index():
    estrenos = obtener_peliculas_proximas()
    peliculas = obtener_peliculas()
    series = obtener_series_proximas()
    series_p = obtener_series_populares()
    return render_template("main/index.html", estrenos=estrenos, peliculas=peliculas, series=series, seriesp=series_p)

@main_bp.route("/peliculas/<categoria>", methods=['GET'])
@main_bp.route("/peliculas/<categoria>/<int:page>", methods=['GET'])
def peliculas_ruta(categoria, page=1):
    # Obtener géneros seleccionados del usuario
    generos = request.args.getlist('selected_genres')
    year = request.args.get('year')
    min_vote = request.args.get('min_vote')

    # Obtener películas y páginas totales según los filtros seleccionados
    peliculas, total_pages = pagina_peliculas(categoria, page, generos, year, min_vote)

    if peliculas is None:
        return "Error al obtener los datos de la API", 500

    # Calcular las páginas a mostrar en el paginador
    if page <= 5:
        start_page = 1
        end_page = min(10, total_pages)
    elif page + 4 > total_pages:
        start_page = max(1, total_pages - 9)
        end_page = total_pages
    else:
        start_page = page - 4
        end_page = page + 5

    # Verificar si es una solicitud AJAX para cargar contenido dinámico
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('main/peliculas_grid.html', peliculas=peliculas, 
                               page=page, start_page=start_page, end_page=end_page, 
                               total_pages=total_pages, categoria=categoria, generos=generos)

    # Renderizar la plantilla principal de películas
    return render_template('main/peliculas.html', 
                           peliculas=peliculas, 
                           categoria=categoria, 
                           page=page, 
                           total_pages=total_pages, 
                           start_page=start_page, 
                           end_page=end_page, 
                           generos=generos, 
                           generos_disponibles=GENEROS_PELICULAS)
    
@main_bp.route("/series/<categoria>", methods=['GET'])
@main_bp.route("/series/<categoria>/<int:page>", methods=['GET'])
def series_ruta(categoria, page=1):
    generos = request.args.getlist('selected_genres')
    year = request.args.get('year')
    min_vote = request.args.get('min_vote')

    series, total_pages = pagina_series(categoria, page, generos, year, min_vote)

    if series is None:
        return "Error al obtener los datos de la API", 500

    if page <= 5:
        start_page = 1
        end_page = min(10, total_pages)
    elif page + 4 > total_pages:
        start_page = max(1, total_pages - 9)
        end_page = total_pages
    else:
        start_page = page - 4
        end_page = page + 5

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('main/series_grid.html', series=series, 
                               page=page, start_page=start_page, end_page=end_page, 
                               total_pages=total_pages, categoria=categoria, generos=generos)

    return render_template('main/pag_series.html', 
                           series=series, 
                           categoria=categoria, 
                           page=page, 
                           total_pages=total_pages, 
                           start_page=start_page, 
                           end_page=end_page, 
                           generos=generos, 
                           generos_disponibles=GENEROS_SERIES)

@main_bp.route('/movie/<int:movie_id>')
def movie(movie_id):
    detalles_pelicula = obtener_detalles_pelicuas(movie_id)
    if detalles_pelicula:
        return render_template("main/movie.html", detalles_pelicula=detalles_pelicula)
    else:
        return "Pelicula no encontrada", 404

@main_bp.route('/series/<int:serie_id>')
def serie(serie_id):
    detalles_series = obtener_detalles_series(serie_id)
    if detalles_series:
        return render_template("main/series.html", detalles_serie=detalles_series)
    else:
        return "Serie no encontrada", 404
    
@main_bp.route("/actores_populares/<int:page>")
def actores_populares(page=1):
    """Ruta que muestra los actores populares con paginación."""
    actores, total_pages = pagina_actores(page)

    # Calcular las páginas a mostrar en el paginador
    if page <= 5:
        start_page = 1
        end_page = min(10, total_pages)
    elif page + 4 > total_pages:
        start_page = max(1, total_pages - 9)
        end_page = total_pages
    else:
        start_page = page - 4
        end_page = page + 5

    return render_template('main/actores_populares.html', actores=actores, page=page, total_pages=total_pages, start_page=start_page, end_page=end_page)
@main_bp.route('fundadores')
def fundadores():
    return render_template("main/fundadores.html")


@main_bp.route('/buscar_pelicula')
def buscar_pelicula():
    query = request.args.get('query')  # Término de búsqueda desde el formulario
    page = request.args.get('page', 1, type=int)  # Página actual, por defecto es 1

    # URLs para buscar en películas, series y actores
    url_peliculas = f'{base_url_api}/search/movie?api_key={api_key}&query={query}&language=en-US&page={page}'
    url_series = f'{base_url_api}/search/tv?api_key={api_key}&query={query}&language=en-US&page={page}'
    url_actores = f'{base_url_api}/search/person?api_key={api_key}&query={query}&language=en-US&page={page}'

    # Hacer las tres solicitudes a la API de TMDB
    response_peliculas = requests.get(url_peliculas)
    response_series = requests.get(url_series)
    response_actores = requests.get(url_actores)

    peliculas, series, actores = [], [], []
    imagen_por_defecto = url_for('static', filename='img/default_image.png', _external=True)
    base_url = 'https://image.tmdb.org/t/p/w500'

    # Procesar la respuesta de películas
    if response_peliculas.status_code == 200:
        data_peliculas = response_peliculas.json()
        peliculas = [
            {
                'id': item['id'],
                'title': item['title'],
                'poster_url': base_url + item['poster_path'] if item.get('poster_path') else imagen_por_defecto,
                'release_date': item.get('release_date', 'Fecha desconocida')
            }
            for item in data_peliculas['results']
        ]

    # Procesar la respuesta de series
    if response_series.status_code == 200:
        data_series = response_series.json()
        series = [
            {
                'id': item['id'],
                'title': item['name'],  # 'name' en lugar de 'title' para series
                'poster_url': base_url + item['poster_path'] if item.get('poster_path') else imagen_por_defecto,
                'release_date': item.get('first_air_date', 'Fecha desconocida')
            }
            for item in data_series['results']
        ]

    # Procesar la respuesta de actores
    if response_actores.status_code == 200:
        data_actores = response_actores.json()
        actores = [
            {
                'id': item['id'],
                'name': item['name'],
                'profile_url': base_url + item['profile_path'] if item.get('profile_path') else imagen_por_defecto,
                'known_for': [known['title'] if 'title' in known else known['name'] for known in item['known_for']]
            }
            for item in data_actores['results']
        ]

    # Renderizar la plantilla con los resultados combinados
    return render_template(
        'main/layout.html',
        query=query,
        peliculas=peliculas,
        series=series,
        actores=actores,
        page=page
    )

