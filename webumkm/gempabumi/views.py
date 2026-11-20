import os
import json
import re
import urllib.request
from datetime import datetime
from pathlib import Path
from django.shortcuts import render

BMKG_URL = "https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json"
CACHE_FILE = Path(__file__).resolve().parent / "data_gempa_cache.json"

def get_kedalaman_info(kedalaman_str):
    """
    Kategori kedalaman gempa:
    - Dangkal: < 70 km (Warna Merah: #e53935)
    - Menengah: 70 - 300 km (Warna Oranye: #f59e0b)
    - Dalam: > 300 km (Warna Hijau: #10b981)
    """
    match = re.search(r"(\d+(?:\.\d+)?)", str(kedalaman_str or ""))
    km = float(match.group(1)) if match else 10.0

    if km < 70:
        return {
            "km": km,
            "kategori": "dangkal",
            "label": "Dangkal (< 70 km)",
            "warna": "#e53935"
        }
    elif km <= 300:
        return {
            "km": km,
            "kategori": "menengah",
            "label": "Menengah (70-300 km)",
            "warna": "#f59e0b"
        }
    else:
        return {
            "km": km,
            "kategori": "dalam",
            "label": "Dalam (> 300 km)",
            "warna": "#10b981"
        }

def gempaterkini(request):
    raw_gempa = []
    waktu_update = datetime.now().strftime("%H.%M.%S")

    # 1. Coba ambil data terbaru secara online dari BMKG
    try:
        req = urllib.request.Request(
            BMKG_URL,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        with urllib.request.urlopen(req, timeout=4) as response:
            payload = json.loads(response.read().decode("utf-8"))
            raw_gempa = payload.get("Infogempa", {}).get("gempa", [])
            # Simpan cache data terkini
            if raw_gempa:
                with open(CACHE_FILE, "w", encoding="utf-8") as f:
                    json.dump(payload, f, ensure_ascii=False, indent=2)
    except Exception:
        # 2. Fallback offline menggunakan cache lokal jika gagal terhubung
        if CACHE_FILE.exists():
            try:
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    payload = json.load(f)
                    raw_gempa = payload.get("Infogempa", {}).get("gempa", [])
            except Exception:
                raw_gempa = []

    # Normalisasi tipe data raw_gempa jika berupa objek tunggal
    if isinstance(raw_gempa, dict):
        raw_gempa = [raw_gempa]
    elif not isinstance(raw_gempa, list):
        raw_gempa = []

    # 3. Proses 15 data gempa untuk template dan peta
    gempa_list = []
    for idx, item in enumerate(raw_gempa[:15]):
        kedalaman_info = get_kedalaman_info(item.get("Kedalaman", "10 km"))
        
        # Koordinat [lat, lng]
        coords_str = item.get("Coordinates", "0,0")
        lat, lng = 0.0, 0.0
        try:
            parts = [float(x.strip()) for x in coords_str.split(",")]
            lat, lng = parts[0], parts[1]
        except Exception:
            lat, lng = 0.0, 0.0

        # Fallback jika parsing Coordinates bernilai 0, coba parse dari Lintang dan Bujur
        if lat == 0.0 and lng == 0.0:
            lintang_str = item.get("Lintang", "")
            bujur_str = item.get("Bujur", "")
            m_lat = re.search(r"(\d+(?:\.\d+)?)\s*(LU|LS)?", lintang_str)
            m_lng = re.search(r"(\d+(?:\.\d+)?)\s*(BT|BB)?", bujur_str)
            if m_lat:
                val_lat = float(m_lat.group(1))
                lat = -val_lat if m_lat.group(2) == "LS" else val_lat
            if m_lng:
                val_lng = float(m_lng.group(1))
                lng = -val_lng if m_lng.group(2) == "BB" else val_lng

        try:
            mag_val = float(item.get("Magnitude", 5.0))
        except ValueError:
            mag_val = 5.0

        data_item = {
            "no": idx + 1,
            "tanggal": item.get("Tanggal", ""),
            "jam": item.get("Jam", ""),
            "datetime": item.get("DateTime", ""),
            "coordinates": coords_str,
            "lat": lat,
            "lng": lng,
            "lintang": item.get("Lintang", ""),
            "bujur": item.get("Bujur", ""),
            "magnitude": item.get("Magnitude", ""),
            "magnitude_val": mag_val,
            "kedalaman": item.get("Kedalaman", ""),
            "kedalaman_km": kedalaman_info["km"],
            "kategori": kedalaman_info["kategori"],
            "kategori_label": kedalaman_info["label"],
            "warna": kedalaman_info["warna"],
            "wilayah": item.get("Wilayah", ""),
            "potensi": item.get("Potensi", ""),
        }
        gempa_list.append(data_item)

    context = {
        "gempa_list": gempa_list,
        "gempa_json": json.dumps(gempa_list),
        "total_gempa": len(gempa_list),
        "waktu_update": waktu_update,
    }

    return render(request, "gempabumi/gempaterkini.html", context)
