from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "cok-gizli-bir-anahtar-bunu-degistir-123456"
ALGORITHM = "HS256"
TOKEN_SURESI_DAKIKA = 60

def sifreyi_hashle(sifre: str) -> str:
    return pwd_context.hash(sifre)

def sifre_dogrula(girilen_sifre: str, hashli_sifre: str) -> bool:
    return pwd_context.verify(girilen_sifre, hashli_sifre)

def token_olustur(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_SURESI_DAKIKA)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def token_dogrula(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None
