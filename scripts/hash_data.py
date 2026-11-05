"""
hash_data.py
============
Verifica que tus CSV de data/raw coincidan con data/SHA256SUMS.txt.
Uso:   python scripts/hash_data.py
Si dice DIFERENTE: vuelve a correr download_data.py (o el archivo se corrompio).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.download_data import sha256  # noqa: E402  reutilizamos la funcion
from src.config import DATA_RAW, ROOT  # noqa: E402


def main():
    sumas = ROOT / "data" / "SHA256SUMS.txt"
    if not sumas.exists():
        print("No hay data/SHA256SUMS.txt. Corre primero scripts/download_data.py")
        sys.exit(1)
    ok = True
    for linea in sumas.read_text(encoding="utf-8").splitlines():
        esperada, nombre = linea.split()          # "huella  archivo"
        real = sha256(DATA_RAW / nombre)
        estado = "OK" if real == esperada else "DIFERENTE"
        ok &= real == esperada
        print(f"[{estado}] {nombre}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
