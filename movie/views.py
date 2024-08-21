from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

from .models import Movie

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html', {'name' : 'Carlos Restrepo'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def about(request):

    #return HttpResponse('<h1>Welcome to About Page</h1>')
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def statistics_view(request):

    matplotlib.use('Agg')
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')  # Obtener todos los 
    # años de las películas.
    movie_counts_by_year = {}  # Crear un diccionario para almacenar la cantidad de películas por año. 
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    bar_width = 8.5  # Ancho de las barras
    bar_spacing = 0.5  # Separación entre las barras
    bar_positions = range(len(movie_counts_by_year))  # Posiciones de las barras

    bar_positions = [(i * (bar_width + bar_spacing)) for i in range(len(movie_counts_by_year))]

    # Crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')

    # Personalizar la gráfica
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)

    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)

    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la gráfica a base64
    image_png_year = buffer.getvalue()
    buffer.close()
    graphic_year = base64.b64encode(image_png_year).decode('utf-8')

    matplotlib.use('Agg')

    # Obtener todos los géneros y contar cuántas películas hay por el primer género
    genres = Movie.objects.values_list('genre', flat=True)
    genre_count = {}

    for genre_list in genres:
        # Considerar solo el primer género
        first_genre = genre_list.split(',')[0].strip()
        if first_genre in genre_count:
            genre_count[first_genre] += 1
        else:
            genre_count[first_genre] = 1

    # Configuración de la gráfica
    bar_width = 0.5
    bar_positions = range(len(genre_count))

    # Crear la gráfica de barras
    plt.bar(bar_positions, genre_count.values(), width=bar_width, align='center')

    # Personalizar la gráfica
    plt.title('Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, genre_count.keys(), rotation=45, ha='right')

    # Ajustar el espaciado entre las barras
    plt.tight_layout()

    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la gráfica a base64
    image_png_genre = buffer.getvalue()
    buffer.close()
    graphic_genre = base64.b64encode(image_png_genre).decode('utf-8')

    # Renderizar la plantilla statistics.html con la gráfica
    return render(request, 'statistics.html', {'graphic_year': graphic_year, 'graphic_genre': graphic_genre})

