from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datos import SessionLocal, engine
from modelos import Base, Personaje
from pydantic import BaseModel

app = FastAPI()

Base.metadata.create_all(bind=engine)


# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic models
class PersonajeCreate(BaseModel):
    nombre: str
    raza: str
    elemento: str


class PersonajeResponse(PersonajeCreate):
    id: int

    class Config:
        orm_mode = True


# Endpoint para crear un personaje
@app.post("/personajes/", response_model=PersonajeResponse)
def crear_personaje(personaje: PersonajeCreate, db: Session = Depends(get_db)):
    db_personaje = Personaje(**personaje.dict())
    db.add(db_personaje)
    db.commit()
    db.refresh(db_personaje)
    return db_personaje


# Endpoint para obtener todos los personajes
@app.get("/personajes/", response_model=list[PersonajeResponse])
def listar_personajes(db: Session = Depends(get_db)):
    return db.query(Personaje).all()


# Endpoint para editar un personaje
@app.put("/personajes/{personaje_id}", response_model=PersonajeResponse)
def editar_personaje(personaje_id: int, personaje: PersonajeCreate, db: Session = Depends(get_db)):
    db_personaje = db.query(Personaje).filter(Personaje.id == personaje_id).first()
    if db_personaje is None:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    for key, value in personaje.dict().items():
        setattr(db_personaje, key, value)
    db.commit()
    db.refresh(db_personaje)
    return db_personaje


# Endpoint para eliminar un personaje
@app.delete("/personajes/{personaje_id}", response_model=PersonajeResponse)
def eliminar_personaje(personaje_id: int, db: Session = Depends(get_db)):
    db_personaje = db.query(Personaje).filter(Personaje.id == personaje_id).first()
    if db_personaje is None:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    db.delete(db_personaje)
    db.commit()
    return db_personaje
