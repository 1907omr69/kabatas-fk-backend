from database import SessionLocal
import models
import auth

db = SessionLocal()

email = input("Admin email: ")
username = input("Admin kullanici adi: ")
password = input("Admin sifresi: ")

mevcut = db.query(models.User).filter(models.User.email == email).first()
if mevcut:
    print("Bu email zaten kayitli!")
else:
    yeni_admin = models.User(
        email=email,
        username=username,
        hashed_password=auth.sifreyi_hashle(password),
        is_admin=True
    )
    db.add(yeni_admin)
    db.commit()
    print(f"Admin kullanici olusturuldu: {username}")

db.close()
