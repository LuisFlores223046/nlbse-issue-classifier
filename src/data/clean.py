"""
clean.py  (responsable: Rogelio)
================================
Funciones de LIMPIEZA de texto. Cada paso es una funcion chica y probada,
y cada decision se anota en docs/decisiones_limpieza.md (eso es trazabilidad).

IMPORTANTE: limpiar NO debe destruir la senal. Ej.: las plantillas de issues
("### Repro steps") pueden delatar la clase; eso se estudia, no se borra a ciegas.
"""

import re  # expresiones regulares: buscar/reemplazar patrones de texto

import pandas as pd  # tablas

# Patrones precompilados (mas rapido y mas legible que escribirlos en cada llamada)
_RE_COMENTARIO_HTML = re.compile(r"<!--.*?-->", flags=re.DOTALL)  # <!-- ... -->
_RE_URL = re.compile(r"https?://\S+")                              # http(s)://lo-que-sea
_RE_BLOQUE_CODIGO = re.compile(r"```.*?```", flags=re.DOTALL)      # ```codigo```
_RE_ESPACIOS = re.compile(r"\s+")                                  # cualquier mezcla de espacios/saltos

URL_TOKEN = " URL "      # en que se convierten los links
CODE_TOKEN = " CODEBLOCK "  # en que se convierten los bloques de codigo


def clean_text(texto, quitar_comentarios_html=True, reemplazar_urls=True,
               reemplazar_codigo=True):
    """Limpia UN texto (titulo o cuerpo) y devuelve el texto limpio.

    Entrada : texto (str o NaN/None).
    Salida  : str (nunca None; si no habia texto devuelve "").
    Por que : los modelos de texto funcionan mejor sin ruido (links largos,
              comentarios invisibles de las plantillas, espacios repetidos).
    """
    # Si viene vacio (NaN de pandas o None), devolvemos cadena vacia para no romper nada.
    if texto is None or (isinstance(texto, float) and pd.isna(texto)):
        return ""
    texto = str(texto)  # por si llegara un numero u otro tipo

    if quitar_comentarios_html:
        texto = _RE_COMENTARIO_HTML.sub(" ", texto)  # los comentarios HTML no los ve el lector
    if reemplazar_codigo:
        texto = _RE_BLOQUE_CODIGO.sub(CODE_TOKEN, texto)  # el codigo largo mete mucho ruido
    if reemplazar_urls:
        texto = _RE_URL.sub(URL_TOKEN, texto)  # el link exacto no importa, que HAY un link si

    texto = _RE_ESPACIOS.sub(" ", texto).strip()  # colapsar espacios y recortar extremos
    return texto


def clean_dataframe(df):
    """Aplica clean_text a title y body y crea la columna `text` (titulo + cuerpo).

    Entrada : DataFrame con columnas repo, created_at, label, title, body.
    Salida  : COPIA del DataFrame con title/body limpios y una columna `text`.
    Por que : los modelos reciben UN solo texto por issue.
    """
    out = df.copy()  # nunca modificamos el original (el crudo es sagrado)
    out["title"] = out["title"].apply(clean_text)
    out["body"] = out["body"].apply(clean_text)
    # El titulo suele ser lo mas informativo: lo ponemos primero.
    out["text"] = (out["title"] + " . " + out["body"]).str.strip()
    return out


def drop_duplicates_report(df):
    """Quita duplicados EXACTOS (mismo repo+titulo+cuerpo) y regresa (df_sin_dup, n_quitados).

    Devolvemos cuantos se quitaron para anotarlo en el reporte (no se oculta nada).
    """
    antes = len(df)
    # keep="first" conserva la primera aparicion y elimina las demas copias
    limpio = df.drop_duplicates(subset=["repo", "title", "body"], keep="first")
    return limpio.reset_index(drop=True), antes - len(limpio)
