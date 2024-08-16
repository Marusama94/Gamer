from datos import engine
from modelos import Base

# Crear todas las tablas definidas en los modelos
Base.metadata.create_all(bind=engine)