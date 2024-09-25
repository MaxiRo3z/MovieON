import requests

api_key = 'cc0bbbd7774ce2853272ceeb3db7db56'
base_url_api = 'https://api.themoviedb.org/3'

def obtener_peliculas_proximas():
    url = f'{base_url_api}/movie/upcoming?api_key={api_key}&language=es-ES&page=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        peliculas = data['results']
        base_url = 'https://image.tmdb.org/t/p/w500'
        peliculas_con_posters = [
            {
                'id': pelicula['id'],
                'title': pelicula['title'],
                'poster_url': base_url + pelicula['poster_path']
            }
            for pelicula in peliculas if pelicula['poster_path']
        ]
        return peliculas_con_posters
    return []

def obtener_peliculas():
    endpoints = [
        f'{base_url_api}/movie/popular?api_key={api_key}&language=es-ES&page=1',
    ]
    peliculas_con_posters = []
    base_url_poster = 'https://image.tmdb.org/t/p/w500'
    ids_ya_agregados = set()

    for url in endpoints:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            peliculas = data['results']
            for pelicula in peliculas:
                ruta_poster = pelicula['poster_path']
                movie_id = pelicula['id']
                if ruta_poster and movie_id not in ids_ya_agregados:
                    url_completa_poster = base_url_poster + ruta_poster
                    peliculas_con_posters.append({
                        'id': movie_id,
                        'titulo': pelicula['title'],
                        'url_poster': url_completa_poster
                    })
                    ids_ya_agregados.add(movie_id)
    return peliculas_con_posters

def pagina_peliculas():
    endpoints = [
        f'{base_url_api}/movie/popular?api_key={api_key}&language=es-ES&page=1',
        f'{base_url_api}/movie/upcoming?api_key={api_key}&language=es-ES&page=1',
        f'{base_url_api}/movie/top_rated?api_key={api_key}&language=es-ES&page=1',
        f'{base_url_api}/movie/now_playing?api_key={api_key}&language=es-ES&page=1',
    ]
    peliculas_con_posters = []
    base_url_poster = 'https://image.tmdb.org/t/p/w500'
    ids_ya_agregados = set()

    for url in endpoints:
        # Repetir por varias páginas
        for page in range(1, 4):  # Ajusta el rango según sea necesario
            response = requests.get(url.replace('page=1', f'page={page}'))  # Cambia la página en la URL
            if response.status_code == 200:
                data = response.json()
                peliculas = data['results']
                for pelicula in peliculas:
                    ruta_poster = pelicula['poster_path']
                    movie_id = pelicula['id']
                    if ruta_poster and movie_id not in ids_ya_agregados:
                        url_completa_poster = base_url_poster + ruta_poster
                        peliculas_con_posters.append({
                            'id': movie_id,
                            'titulo': pelicula['title'],
                            'url_poster': url_completa_poster
                        })
                        ids_ya_agregados.add(movie_id)

    return peliculas_con_posters

def obtener_series_proximas():
    url = f'{base_url_api}/tv/on_the_air?api_key={api_key}&language=es-ES&page=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        series = data['results']
        base_url = 'https://image.tmdb.org/t/p/w500'
        series_con_posterso = [
            {
                'id': serie['id'],
                'title': serie['name'],  # Para series, el campo es 'name'
                'poster_url': base_url + serie['poster_path']
            }
            for serie in series if serie['poster_path']
        ]
        return series_con_posterso
    return []

def obtener_series_populares():
    url = f'{base_url_api}/tv/popular?api_key={api_key}&language=es-ES&page=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        series = data['results']
        base_url = 'https://image.tmdb.org/t/p/w500'
        series_con_postersp = [
            {
                'id': serie['id'],
                'title': serie['name'],  # Para series, el campo es 'name'
                'poster_url': base_url + serie['poster_path']
            }
            for serie in series if serie['poster_path']
        ]
        return series_con_postersp
    return []

def obtener_detalles_pelicuas(movie_id):
    base_url_poster = 'https://image.tmdb.org/t/p/w500'
    base_url_backdrop = 'https://image.tmdb.org/t/p/original'
    response = requests.get(f"{base_url_api}/movie/{movie_id}?api_key={api_key}&language=es-ES")
    credits_response = requests.get(f"{base_url_api}/movie/{movie_id}/credits?api_key={api_key}&language=es-ES")
    if response.status_code == 200 and credits_response.status_code == 200:
        data = response.json()
        credits_data = credits_response.json()

        # Filtrar el equipo (crew) para obtener director y guionista
        crew = credits_data['crew']
        directores = [person['name'] for person in crew if person['job'] == 'Director']
        guionistas = [person['name'] for person in crew if person['job'] in ['Screenplay', 'Writer']]

        detalles_pelicula = {
            'titulo_pelicula': data['title'],
            'anio_estreno': data['release_date'][:4],
            'clasificacion': 'PG-13' if data['adult'] else 'PG',
            'fecha_estreno': data['release_date'],
            'generos': ', '.join([g['name'] for g in data['genres']]),
            'duracion': f"{data['runtime']} mins",
            'puntuacion_usuario': int(data['vote_average'] * 10),
            'resumen_pelicula': data['overview'],
            'director': ','.join(directores) if directores else 'Desconocido',  # Añadir lógica para obtener el director
            'guionista': ','.join(guionistas) if guionistas else 'Desconocido',  # Añadir lógica para obtener el guionista
            'url_poster': base_url_poster + data['poster_path'],
            'url_backdrop': base_url_backdrop + data['backdrop_path'] if data['backdrop_path'] else None  # Imagen de fondo
        }
        return detalles_pelicula
    
def obtener_detalles_series(serie_id):
    base_url_poster = 'https://image.tmdb.org/t/p/w500'
    base_url_backdrop = 'https://image.tmdb.org/t/p/original'

    response = requests.get(f"{base_url_api}/tv/{serie_id}?api_key={api_key}&language=es-ES")
    credits_response = requests.get(f"{base_url_api}/tv/{serie_id}/credits?api_key={api_key}&language=es-ES")
    
    if response.status_code == 200 and credits_response.status_code == 200:
        data = response.json()
        credits_data = credits_response.json()

        # Filtrar el equipo (crew) para obtener director y guionista
        crew = credits_data['crew']
        directores = [person['name'] for person in crew if person['job'] == 'Director']
        guionistas = [person['name'] for person in crew if person['job'] in ['Screenplay', 'Writer']]

        detalles_serie = {
            'titulo_pelicula': data['name'],
            'anio_estreno': data['first_air_date'][:4],
            'clasificacion': 'PG-13' if data['adult'] else 'PG',
            'fecha_estreno': data['first_air_date'],
            'generos': ', '.join([g['name'] for g in data['genres']]),
            'duracion': f"{data['episode_run_time'][0]} mins" if data['episode_run_time'] else 'Desconocido',
            'puntuacion_usuario': int(data['vote_average'] * 10),
            'resumen_pelicula': data['overview'],
            'director': ','.join(directores) if directores else 'Desconocido',  # Añadir lógica para obtener el director
            'guionista': ','.join(guionistas) if guionistas else 'Desconocido',  # Añadir lógica para obtener el guionista
            'url_poster': base_url_poster + data['poster_path'],
            'url_backdrop': base_url_backdrop + data['backdrop_path'] if data['backdrop_path'] else None  # Imagen de fondo
        }
    return detalles_serie