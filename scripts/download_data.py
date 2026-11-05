"""
download_data.py
================
Descarga los CSV oficiales de NLBSE'24 a data/raw/ y guarda sus huellas SHA-256
en data/SHA256SUMS.txt.  Uso:   python scripts/download_data.py

Por que: la licencia del repo oficial esta vacia, asi que NO subimos los CSV a
nuestro repo; cada quien los baja de la fuente. El SHA-256 prueba que todos
tenemos EXACTAMENTE los mismos datos (trazabilidad).
"""

import hashlib
import sys
import urllib.request  # biblioteca estandar: no requiere instalar nada
from pathlib import Path

# Permite correr el script desde cualquier carpeta
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.config import DATA_RAW, ROOT, TEST_RAW, TEST_URL, TRAIN_RAW, TRAIN_URL  # noqa: E402


def sha256(ruta):
    """Huella digital del archivo: si cambia un solo byte, cambia la huella."""
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):  # leer de 1 MB en 1 MB
            h.update(bloque)
    return h.hexdigest()


def main():
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    lineas = []
    for url, destino in ((TRAIN_URL, TRAIN_RAW), (TEST_URL, TEST_RAW)):
        print(f"Descargando {url} ...")
        urllib.request.urlretrieve(url, destino)  # baja y guarda
        huella = sha256(destino)
        print(f"  -> {destino.name}  {destino.stat().st_size} bytes  sha256={huella}")
        lineas.append(f"{huella}  {destino.name}")
    (ROOT / "data" / "SHA256SUMS.txt").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print("Listo. Huellas en data/SHA256SUMS.txt (esas SI se suben a git).")


if __name__ == "__main__":
    main()
