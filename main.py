from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from sqlalchemy.orm import Session
from typing import List
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

import models
import schemas
from database import SessionLocal, engine
from weather_api import obter_dados_climaticos

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Middleware para lidar com CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitações de todos os origens, você pode ajustar conforme necessário
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)


# Manipulador de exceção para retornar erros de validação de solicitação como JSON
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"message": "Erro de validação", "details": exc.errors()},
    )


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/dados-climaticos/", response_model=schemas.WeatherData)
def criar_dado_climatico(dados_climaticos: schemas.WeatherDataCreate, db: Session = Depends(get_db)):
    db_dados_climaticos = models.WeatherData(**dados_climaticos.dict())
    db.add(db_dados_climaticos)
    db.commit()
    db.refresh(db_dados_climaticos)
    return db_dados_climaticos


@app.get("/dados-climaticos/", response_model=List[schemas.WeatherData])
def listar_dados_climaticos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    dados_climaticos = db.query(models.WeatherData).offset(skip).limit(limit).all()
    return dados_climaticos


@app.get("/dados-climaticos/{dados_climaticos_id}", response_model=schemas.WeatherData)
def detalhar_dado_climatico(dados_climaticos_id: int, db: Session = Depends(get_db)):
    dado_climatico = db.query(models.WeatherData).filter(models.WeatherData.id == dados_climaticos_id).first()
    if dado_climatico is None:
        raise HTTPException(status_code=404, detail="Dados climáticos não encontrados")
    return dado_climatico


@app.put("/dados-climaticos/{dados_climaticos_id}", response_model=schemas.WeatherData)
def editar_dado_climatico(dados_climaticos_id: int, dados_climaticos: schemas.WeatherDataCreate,
                          db: Session = Depends(get_db)):
    db_dados_climaticos = db.query(models.WeatherData).filter(models.WeatherData.id == dados_climaticos_id).first()
    if db_dados_climaticos is None:
        raise HTTPException(status_code=404, detail="Dados climáticos não encontrados")
    for key, value in dados_climaticos.dict().items():
        setattr(db_dados_climaticos, key, value)
    db.commit()
    db.refresh(db_dados_climaticos)
    return db_dados_climaticos


@app.delete("/dados-climaticos/{dados_climaticos_id}", response_model=schemas.WeatherData)
def deletar_dado_climatico(dados_climaticos_id: int, db: Session = Depends(get_db)):
    db_dados_climaticos = db.query(models.WeatherData).filter(models.WeatherData.id == dados_climaticos_id).first()
    if db_dados_climaticos is None:
        raise HTTPException(status_code=404, detail="Dados climáticos não encontrados")
    db.delete(db_dados_climaticos)
    db.commit()
    return db_dados_climaticos



@app.post("/buscar-salvar-clima/", response_model=schemas.WeatherData)
def buscar_e_salvar_dados_climaticos(dados: schemas.CityData, db: Session = Depends(get_db)):
    cidade = dados.cidade
    dados_climaticos = obter_dados_climaticos(cidade)
    if not dados_climaticos:
        raise HTTPException(status_code=404, detail="Não foi possível obter os dados climáticos")

    formatted_data = {
        "city": dados_climaticos["name"],
        "country": dados_climaticos["sys"]["country"],
        "temperature": dados_climaticos["main"]["temp"],
        "humidity": dados_climaticos["main"]["humidity"],
        "pressure": dados_climaticos["main"]["pressure"],
        "wind_speed": dados_climaticos["wind"]["speed"],
        "wind_deg": dados_climaticos["wind"]["deg"],
        "description": dados_climaticos["weather"][0]["description"],
        "visibility": dados_climaticos["visibility"],
        "sunrise": datetime.fromtimestamp(dados_climaticos["sys"]["sunrise"]).strftime('%Y-%m-%d %H:%M:%S'),
        "sunset": datetime.fromtimestamp(dados_climaticos["sys"]["sunset"]).strftime('%Y-%m-%d %H:%M:%S'),
        "timestamp": datetime.fromtimestamp(dados_climaticos["dt"]).strftime('%Y-%m-%d %H:%M:%S')
    }

    db_dados_climaticos = models.WeatherData(**formatted_data)
    db.add(db_dados_climaticos)
    db.commit()
    db.refresh(db_dados_climaticos)
    return db_dados_climaticos


# Rota para o Swagger UI
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Documentação da API")


# Rota para o arquivo JSON OpenAPI
@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return JSONResponse(get_openapi(title="Documentação da API", version="0.1.0", routes=app.routes))
