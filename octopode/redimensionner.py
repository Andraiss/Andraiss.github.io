"""
Redimensionne les photos pour le site.

Usage
  pip install pillow
  python redimensionner.py dossier_photos_originales

Pour chaque photo (jpg, jpeg, png, heic exclu), crée dans images/
  nom.jpg      grande version, 1600 px max, ouverte au clic
  nom-800.jpg  petite version, 800 px max, affichée sur la page

Renomme tes photos AVANT de lancer le script avec les noms attendus par
index.html (proto-v1, proto-v2, proto-v3, final, galerie-1 ... galerie-6,
og-cover), ou adapte les noms dans index.html.
"""
import sys
from pathlib import Path
from PIL import Image, ImageOps

GRANDE = 1600     # px, côté le plus long
PETITE = 800      # px
QUALITE = 82      # qualité JPEG (70-90)

src = Path(sys.argv[1] if len(sys.argv) > 1 else "originales")
out = Path(__file__).parent / "images"
out.mkdir(exist_ok=True)

for p in sorted(src.iterdir()):
    if p.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
        continue
    im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
    for taille, suffixe in ((GRANDE, ""), (PETITE, "-800")):
        c = im.copy()
        c.thumbnail((taille, taille), Image.LANCZOS)
        dest = out / f"{p.stem}{suffixe}.jpg"
        c.save(dest, "JPEG", quality=QUALITE, optimize=True, progressive=True)
        print(f"{dest.name:28s} {c.size[0]}x{c.size[1]}  {dest.stat().st_size // 1024} ko")

    if p.stem == "og-cover":   # image d'aperçu des liens, format 1200x630
        c = ImageOps.fit(im, (1200, 630), Image.LANCZOS)
        c.save(out / "og-cover.jpg", "JPEG", quality=QUALITE, optimize=True)
