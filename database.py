from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Veritabanı dosyamızın adı ve konumu
DATABASE_URL = "sqlite:///./futbol.db"

# Veritabanı motorunu oluşturuyoruz
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Veritabanıyla konuşmak için oturum (session) oluşturucu
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tablolarımızın temel sınıfı (base class)
Base = declarative_base()