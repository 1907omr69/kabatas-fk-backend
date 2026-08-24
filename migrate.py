import json
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

with open("kabatasfc-cebe8-default-rtdb-export.json", encoding="utf-8") as f:
    data = json.load(f)

kd = data["kabatasData"]
db = SessionLocal()

def oyuncu_aktar(oyuncu_listesi, takim_adi):
    for o in oyuncu_listesi:
        yeni_oyuncu = models.Player(
            team=takim_adi,
            no=str(o.get("no", "")),
            name=o.get("name", ""),
            username=o.get("username", None),
            hashed_password=o.get("password", None),
            goals=o.get("goals", 0),
            assists=o.get("assists", 0),
            matches=o.get("matches", 0),
            photo_path=None
        )
        db.add(yeni_oyuncu)
    db.commit()
    print(f"{takim_adi} takimi aktarildi: {len(oyuncu_listesi)} oyuncu")

oyuncu_aktar(kd.get("aTeam", []), "A")
oyuncu_aktar(kd.get("bTeam", []), "B")

for m in kd.get("pastMatches", []):
    yeni_mac = models.Match(description=m, status="past")
    db.add(yeni_mac)

for m in kd.get("futureMatches", []):
    yeni_mac = models.Match(description=m, status="future")
    db.add(yeni_mac)

db.commit()
print("Maclar aktarildi")

for c in kd.get("chat", []):
    yeni_mesaj = models.ChatMessage(
        sender_name=c.get("sender", ""),
        sender_id=str(c.get("senderId", "")),
        text=c.get("text", ""),
        sent_at=str(c.get("time", ""))
    )
    db.add(yeni_mesaj)

db.commit()
print("Sohbet mesajlari aktarildi")

tactics = kd.get("tactics", {})
for takim_adi, t in tactics.items():
    yeni_taktik = models.Tactic(
        team=takim_adi,
        formation=t.get("formation", ""),
        slots=t.get("slots", [])
    )
    db.add(yeni_taktik)

db.commit()
print("Taktikler aktarildi")

db.close()
print("Tum veri aktarimi tamamlandi!")
