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
    peliculas, total_pages = pagina_peliculas(categoria, page)

    # Calcular las páginas a mostrar
    if page <= 5:
        start_page = 1
        end_page = min(10, total_pages)  # Mostrar hasta 10 páginas
    elif page + 4 > total_pages:
        start_page = max(1, total_pages - 9)  # Asegurarse de no exceder el total
        end_page = total_pages
    else:
        start_page = page - 4  # Mostrar 4 páginas antes
        end_page = page + 5  # Mostrar 5 páginas después

    return render_template('main/peliculas.html', peliculas=peliculas, categoria=categoria, page=page, total_pages=total_pages, start_page=start_page, end_page=end_page)
    
@main_bp.route("/series/<categoria>", methods=['GET'])
@main_bp.route("/series/<categoria>/<int:page>", methods=['GET'])
def series_ruta(categoria, page=1):
    series, total_pages = pagina_series(categoria, page)

    # Calcular las páginas a mostrar
    if page <= 5:
        start_page = 1
        end_page = min(10, total_pages)  # Mostrar hasta 10 páginas
    elif page + 4 > total_pages:
        start_page = max(1, total_pages - 9)  # Asegurarse de no exceder el total
        end_page = total_pages
    else:
        start_page = page - 4  # Mostrar 4 páginas antes
        end_page = page + 5  # Mostrar 5 páginas después

    return render_template('main/pag_series.html', series=series, categoria=categoria, page=page, total_pages=total_pages, start_page=start_page, end_page=end_page)
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
@cache.cached(timeout=300, query_string=True)
def buscar_pelicula():
    query = request.args.get('query')  # Término de búsqueda desde el formulario
    page = request.args.get('page', 1, type=int)  # Página actual, por defecto es 1
    peliculas, series, actores = buscar_peli(query, page)  # Llama a la función del servicio
    return render_template('main/layout.html', query=query, peliculas=peliculas, series=series, actores=actores, page=page)

