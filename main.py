from flask import Flask,render_template
import requests

api_key= 'cc0bbbd7774ce2853272ceeb3db7db56'

def obtener_peliculas_proximas():
    url = f'https://api.themoviedb.org/3/movie/upcoming?api_key={api_key}&language=es-ES&page=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        peliculas = data['results']
        base_url = 'https://image.tmdb.org/t/p/w500'
        peliculas_con_posters = []
        for pelicula in peliculas:
            poster_path = pelicula['poster_path']
            if poster_path:
                full_poster_url = base_url + poster_path
                peliculas_con_posters.append({
                    'title': pelicula['title'],
                    'poster_url': full_poster_url
                })
        return peliculas_con_posters
    else:
        return []

def obtener_peliculas():
    # Endpoints para películas en emisión y populares
    endpoints = [
        f'https://api.themoviedb.org/3/movie/now_playing?api_key={api_key}&language=es-ES&page=1',
        f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=es-ES&page=1',
        
    ]
    
    peliculas_con_posters = []
    base_url_poster = 'https://image.tmdb.org/t/p/w500'
    
    for url in endpoints:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            peliculas = data['results']
            for pelicula in peliculas:
                ruta_poster = pelicula['poster_path']
                if ruta_poster:
                    url_completa_poster = base_url_poster + ruta_poster
                    peliculas_con_posters.append({
                        'titulo': pelicula['title'],
                        'url_poster': url_completa_poster
                    })
    
    return peliculas_con_posters

app= Flask(__name__)

@app.route("/")
def index():
    estrenos= obtener_peliculas_proximas()
    peliculas= obtener_peliculas()
    return render_template("index.html", estrenos=estrenos, peliculas=peliculas)

@app.route("/login")
def login():
    return render_template("inicio_sesion.html")

@app.route("/register")
def register():
    return render_template("registro.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)