from database import SessionLocal
import models
import auth

db = SessionLocal()

oyuncular = db.query(models.Player).all()

sayac = 0
for oyuncu in oyuncular:
    if oyuncu.hashed_password and not oyuncu.hashed_password.startswith("$"):
        duz_sifre = oyuncu.hashed_password
        oyuncu.hashed_password = auth.sifreyi_hashle(duz_sifre)
        sayac += 1

db.commit()
db.close()
print(f"{sayac} oyuncunun sifresi hashlendi!")
