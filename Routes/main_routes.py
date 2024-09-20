from flask import render_template
from services.api_service import obtener_peliculas_proximas, obtener_peliculas, obtener_detalles_pelicuas,obtener_series_proximas,obtener_series_populares,pagina_peliculas

from . import main_bp

@main_bp.route("/")
def index():
    estrenos = obtener_peliculas_proximas()
    peliculas = obtener_peliculas()
    series= obtener_series_proximas()
    series_p= obtener_series_populares()
    return render_template("main/index.html", estrenos=estrenos, peliculas=peliculas,series=series, seriesp=series_p)

@main_bp.route("/peliculas")
def peliculas():
    peliculas= pagina_peliculas()
    return render_template('main/peliculas.html',peliculas=peliculas)

@main_bp.route('/movie/<int:movie_id>')
def movie(movie_id):
    detalles_pelicula = obtener_detalles_pelicuas(movie_id)
    if detalles_pelicula:
        return render_template("main/movie.html", movie=detalles_pelicula)
    else:
        return "Pelicula no encontrada", 404
    
