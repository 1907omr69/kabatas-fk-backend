from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
import auth
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def gecerli_kullanici(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    email = auth.token_dogrula(token)
    if email is None:
        raise HTTPException(status_code=401, detail="Gecersiz veya suresi dolmus token")

    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user is None:
        raise HTTPException(status_code=401, detail="Kullanici bulunamadi")

    return db_user

@app.get("/")
def anasayfa():
    return {"mesaj": "Backend calisiyor!"}

@app.post("/register", response_model=schemas.UserResponse)
def kayit_ol(user: schemas.UserCreate, db: Session = Depends(get_db)):
    mevcut_kullanici = db.query(models.User).filter(models.User.email == user.email).first()
    if mevcut_kullanici:
        raise HTTPException(status_code=400, detail="Bu e-posta zaten kayitli")

    hashli_sifre = auth.sifreyi_hashle(user.password)

    yeni_kullanici = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashli_sifre
    )

    db.add(yeni_kullanici)
    db.commit()
    db.refresh(yeni_kullanici)

    return yeni_kullanici

@app.post("/login")
def giris_yap(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user or not auth.sifre_dogrula(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Email veya sifre hatali")

    token = auth.token_olustur({"sub": db_user.email})

    return {"access_token": token, "token_type": "bearer", "mesaj": f"Hos geldin, {db_user.username}!"}

@app.get("/me", response_model=schemas.UserResponse)
def benim_bilgilerim(current_user: models.User = Depends(gecerli_kullanici)):
    return current_user

@app.get("/players", response_model=List[schemas.PlayerResponse])
def oyunculari_listele(db: Session = Depends(get_db)):
    oyuncular = db.query(models.Player).all()
    return oyuncular

@app.get("/players/{team}", response_model=List[schemas.PlayerResponse])
def takim_oyunculari(team: str, db: Session = Depends(get_db)):
    oyuncular = db.query(models.Player).filter(models.Player.team == team.upper()).all()
    return oyuncular

@app.get("/matches")
def maclari_listele(db: Session = Depends(get_db)):
    maclar = db.query(models.Match).all()
    return maclar

@app.get("/site-data")
def site_verisini_getir(db: Session = Depends(get_db)):
    kayit = db.query(models.SiteData).filter(models.SiteData.key == "kabatasData").first()
    if kayit is None:
        return None
    return kayit.value

@app.post("/site-data")
def site_verisini_kaydet(veri: dict = Body(...), db: Session = Depends(get_db)):
    kayit = db.query(models.SiteData).filter(models.SiteData.key == "kabatasData").first()
    if kayit is None:
        kayit = models.SiteData(key="kabatasData", value=veri)
        db.add(kayit)
    else:
        kayit.value = veri
    db.commit()
    return {"mesaj": "Kaydedildi"}

@app.post("/admin-login")
def admin_giris(bilgiler: dict = Body(...), db: Session = Depends(get_db)):
    email = bilgiler.get("email")
    password = bilgiler.get("password")

    db_user = db.query(models.User).filter(models.User.email == email).first()

    if not db_user or not db_user.is_admin or not auth.sifre_dogrula(password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Gecersiz admin bilgileri")

    token = auth.token_olustur({"sub": db_user.email})

    return {"access_token": token, "mesaj": "Admin girisi basarili"}
