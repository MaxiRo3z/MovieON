from flask import render_template, request
import math
from services.api_service import *

from . import main_bp

@main_bp.route("/")
def index():
    estrenos = obtener_peliculas_proximas()
    peliculas = obtener_peliculas()
    series= obtener_series_proximas()
    series_p= obtener_series_populares()
    return render_template("main/index.html", estrenos=estrenos, peliculas=peliculas,series=series, seriesp=series_p)

@main_bp.route("/peliculas")
def peliculas_ruta():
    # Obtener todas las películas y el total
    peliculas, total_peliculas = pagina_peliculas()  # Esto ahora debería funcionar correctamente

    # Definir cuántas mostrar por página
    peliculas_por_pagina = 20

    # Calcular el total de páginas
    total_paginas = math.ceil(total_peliculas / peliculas_por_pagina)

    # Obtener la página actual desde la URL; si no existe, iniciar en la 1
    pagina_actual = int(request.args.get('pagina', 1))

    # Calcular el índice de inicio y fin para las películas de la página actual
    inicio = (pagina_actual - 1) * peliculas_por_pagina
    fin = inicio + peliculas_por_pagina

    # Obtener las películas para la página actual
    peliculas_actuales = peliculas[inicio:fin]

    return render_template('main/peliculas.html', peliculas=peliculas_actuales, pagina_actual=pagina_actual, total_paginas=total_paginas)

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
        return "Pelicula no encontrada", 404
