from flask import render_template, request
import math
from services.api_service import *
from . import main_bp
from cache_config import cache  # Importa cache aquí

@main_bp.route("/")
def index():
    estrenos = obtener_peliculas_proximas()
    peliculas = obtener_peliculas()
    series = obtener_series_proximas()
    series_p = obtener_series_populares()
    return render_template("main/index.html", estrenos=estrenos, peliculas=peliculas, series=series, seriesp=series_p)

@main_bp.route("/peliculas/<categoria>/<int:page>")
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


@main_bp.route("/series/<categoria>/<int:page>")
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
