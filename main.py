from fastapi import FastAPI, Body, Path, Query, Request, Depends
from fastapi.security.http import HTTPAuthorizationCredentials,HTTPException
from pydantic import BaseModel, Field
from typing import Optional,List
from fastapi.responses import JSONResponse
from jwt_manager import create_token,validate_token
from fastapi.security import HTTPBearer

from config.database import Session, engine, Base
from models.movie import Movie as MovieModel

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["user"] != "jbosch":
            raise HTTPException(statuscode=403, detail="Credenciales incorrectas")
        return await super().__call__(request)



class Movie(BaseModel):
    id: Optional[int] = None 
    title: str = Field(min_length=5, max_length=20)
    overview: str = Field(min_length=15, max_length=120)
    year: int = Field( le=2024)
    rating: float
    category: str = Field(min_length=4, max_length=520)

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

class User(BaseModel):
    user: str
    password: str


app = FastAPI()
app.title= "Mi aplicación con FastAPI"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)

@app.get('/', tags=["Home"])
def message():
    return "Hola Mundo"

@app.post('/', tags=["Auth"])
def login(usuario: User):
    if usuario.user == "jbosch" and usuario.password=="admin":
        token : str = create_token(usuario.dict())
        return JSONResponse(status_code=200, content=token)
    return JSONResponse(status_code=420, content="")

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


@app.get('/movies', tags=["Movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
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
    

@app.post('/movies', tags=["Movies"], response_model=dict, status_code=201)
def add_movie(movie:Movie)-> dict:
    db = Session()
    try:
      new_movie = MovieModel(**movie.model_dump())
      db.add(new_movie)
      db.commit()
      db.refresh(new_movie)  # Asegúrate de refrescar el objeto
      return {"message": "Película agregada exitosamente"}
    except Exception as e:
        db.rollback()  # En caso de error, hace rollback
        raise HTTPException(status_code=500, detail=str(e))  # Devuelve el error
    finally:
        db.close()  # Cierra la sesión

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