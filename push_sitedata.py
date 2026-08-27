import json
import requests

with open("kabatasfc-cebe8-default-rtdb-export.json", encoding="utf-8") as f:
    data = json.load(f)

kd = data["kabatasData"]

response = requests.post(
    "https://kabatas-fk-backend.onrender.com/site-data",
    json=kd
)

print("Durum kodu:", response.status_code)
print("Cevap:", response.text[:200])
