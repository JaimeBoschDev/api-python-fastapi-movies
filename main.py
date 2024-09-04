from fastapi import FastAPI, Body, Path, Query
from pydantic import BaseModel, Field
from typing import Optional,List
from fastapi.responses import JSONResponse

class Movie(BaseModel):
    id: Optional[int] | None
    title: str = Field(min_length=5, max_length=20)
    overview: str = Field(min_length=15, max_length=120)
    year: int = Field( le=2024)
    rating: float
    category: str = Field(min_length=15, max_length=520)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Titulo",
                "overview": "Descripción de la pelicula",
                "year": "2024",
                "rating": 7.8,
                "category": "Acción"
            }
        }

app = FastAPI()
app.title= "Mi aplicación con FastAPI"
app.version = "0.0.1"

@app.get('/', tags=["Home"])
def message():
    return "Hola Mundo"


movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },
    {
        "id": 2,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2019",
        "rating": 7.8,
        "category": "Drama"
    },
      {
        "id": 3,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },
     {
        "id": 4,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2019",
        "rating": 7.8,
        "category": "Drama"
    },
]


@app.get('/movies', tags=["Movies"], response_model=List[Movie], status_code=200)
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content= movies)

@app.get('/movies/', tags=["Movies"])
def get_movies(category : str = Query(min_length=5, max_length=15)):
    movie_Filter=[]
    '''
    for movie in movies:
        if movie["category"] == category:
            movie_Filter.append(movie)
    return movie_Filter
    '''
    return [item for item in movies if item["category"]== category ]

@app.get('/movies/{id}', tags=["Movies"])
def get_movie(id: int = Path(le=2000, ge=0)):
    for item in movies:
        if item["id"] == id:
            return item
        return []
    

@app.post('/movies', tags=["Movies"])
def add_movie(movie:Movie = Body()):
    movies.append({
        "id": movie.id,
           "title": movie.title,
           "overview": movie.overview,
           "year": movie.year,
           "rating": movie.rating,
           "category": movie.category
    })
    return movies

@app.put('/movies', tags=["Movies"])
def add_movie(id: int , movie:Movie = Body()):
    for item in movies:
        if item["id"]==id:
           item["title"]= movie.title
           item["overview"]= movie.overview
           item["year"]= movie.year
           item["rating"]= movie.rating
           item["category"]= movie.category

  #  posicion = next((index for index, pelicula in enumerate(movies) if pelicula["id"] == id), None)
    return movies

@app.delete('/movies/{id}', tags=["Movies"])
def get_movie(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
        return movies