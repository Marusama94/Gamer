from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# URL de conexión a la base de datos MySQL (XAMPP)
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/skin"

# Crear el motor (engine) de la base de datos
engine = create_engine(DATABASE_URL)

# Crear una clase de sesión que nos permitirá interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

