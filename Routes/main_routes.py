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
    return render_template('main/peliculas.html', peliculas=peliculas, categoria=categoria, page=page, total_pages=total_pages)

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