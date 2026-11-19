# Obtención de datos mediante API: Deezer

Este documento recoge la información del apartado 2 del enunciado sobre la parte de la API: qué API se ha elegido y por qué, qué aporta, qué direcciones se consultan, qué campos se recogen, cómo se hace la consulta y en qué condiciones.

El código está en `api/api_deezer.py` (obtención) y `api/dataframe_api.py` (preparación).

---

## 1. API elegida y motivos

**API pública de Deezer**

- Dirección base: `https://api.deezer.com`
- Documentación: https://developers.deezer.com/api

Motivos de la elección:

- **Es gratuita y no pide clave, registro ni OAuth** para consultar el catálogo: búsqueda, canciones, álbumes y artistas. Basta con una petición GET.
- **Responde en JSON sencillo**, que se lee directamente con `requests` y `pandas`.
- **Tiene un límite de peticiones razonable**, de unas 50 cada 5 segundos. Permite consultar las 1.522 canciones distintas del periodo 2005-2025 en una sola ejecución.
- **Tiene buena cobertura de música comercial británica e internacional**, la que aparece en las listas de Official Charts.

### Alternativas que se descartaron

| API | Motivo del descarte |
|---|---|
| Spotify Web API | Necesita registrar una aplicación y hacer autenticación OAuth. Desde el 27 de noviembre de 2024 las aplicaciones nuevas no pueden usar los endpoints más interesantes, como *audio features* (tempo, energía o bailabilidad), ni las recomendaciones. |
| MusicBrainz | Es gratuita y abierta, pero limita a 1 petición por segundo y obliga a identificarse con un User-Agent. Su modelo de datos (grabación, publicación, grupo de publicaciones) es más complejo de cruzar. Queda como posible ampliación para obtener el país de origen de los artistas. |
| Last.fm | Necesita pedir una clave de API. Sus datos (etiquetas y número de escuchas) son de otro tipo. |

---

## 2. Qué aporta la API al estudio

El web scraping de Official Charts da, para cada año, la **posición**, el **título**, el **artista**, el **pico** y las **semanas**. Desde la ficha de cada canción saca también el **sello** (`label`), el **número de catálogo** y una fecha (`primera_fecha`). La API completa esos datos con características de cada canción y de cada artista que Official Charts no tiene:

| Pregunta del proyecto | Cómo ayuda Deezer |
|---|---|
| **Sellos discográficos (labels)** | El sello principal sale del scraping. Deezer da el `label` del lanzamiento en la plataforma (`sello_deezer`), que sirve para **contrastar** el dato de Official Charts y para **completar** las canciones en las que falte. |
| **Canciones más longevas** | Deezer da la fecha de **lanzamiento** (`release_date`). Restándola al año de la lista se calcula cuántos años después de salir sigue una canción en la lista de fin de año, y se distinguen los éxitos del año de los clásicos que vuelven a entrar. |
| **Artistas más destacados** | Además de contar sus apariciones en las listas, se puede comparar con su número de seguidores en Deezer (`nb_fan`) y con la popularidad actual de sus canciones (`rank`). |
| **Descripción de las canciones** | Duración, letra explícita, género y tipo de lanzamiento (single, álbum o EP). Permiten estudiar, por ejemplo, si las canciones de éxito son cada vez más cortas. |

---

## 3. Direcciones consultadas

| Endpoint | Para qué se usa | Ejemplo |
|---|---|---|
| `GET /search?q=...&limit=5` | Buscar la canción a partir del título y el artista de Official Charts | `https://api.deezer.com/search?q=CRAZY FROG AXEL F&limit=5` |
| `GET /album/{id}` | Sello, género, tipo y fecha del lanzamiento | `https://api.deezer.com/album/302127` |
| `GET /artist/{id}` | Seguidores del artista | `https://api.deezer.com/artist/27` |

**Fecha de obtención:** 19 de noviembre de 2026. También se guarda en la columna `fecha_obtencion` del CSV.

---

## 4. Campos recogidos

| Variable | Origen en la API | Tipo | Unidad |
|---|---|---|---|
| `titulo`, `artista` | del scraping (clave para unir las dos fuentes) | texto | – |
| `encontrada` | calculado en el código | booleana | – |
| `deezer_titulo`, `deezer_artista` | `search.data[].title`, `.artist.name` | texto | – |
| `duracion_s` | `search.data[].duration` | numérica discreta | segundos |
| `explicita` | `search.data[].explicit_lyrics` | booleana | – |
| `popularidad_deezer` | `search.data[].rank` | numérica discreta | puntos de popularidad |
| `sello_deezer` | `album.label` | categórica | – |
| `fecha_lanzamiento` | `album.release_date` | fecha | AAAA-MM-DD |
| `tipo_lanzamiento` | `album.record_type` | categórica | single / album / ep / compile |
| `genero` | primer género de `album.genres` | categórica | – |
| `artista_fans` | `artist.nb_fan` | numérica discreta | personas |
| `fecha_obtencion` | calculado en el código | fecha | AAAA-MM-DD |

---

## 5. Procedimiento

1. **Entrada:** el fichero del web scraping (`officialcharts_2005_2025.csv`). Se lee línea a línea: las líneas `AAAA canciones:` indican el año y el resto son canciones con los campos separados por `|`.
2. **Canciones únicas:** una misma canción puede aparecer en varios años, así que se busca una sola vez cada pareja título + artista (1.522 canciones distintas de 2.100 filas).
3. **Búsqueda:** se busca en Deezer el texto `artista título`, igual que en su buscador, usando solo el **artista principal** (lo que va antes de `FT`, `X`, `&`, `/` o `,`). De los 5 primeros resultados se toma el primero cuyo título **contiene el título de Official Charts o está contenido en él** (sin distinguir mayúsculas). Si ninguno coincide, la canción se marca como no encontrada (`encontrada = False`).

   *Cambio de criterio:* en la primera versión se usaba la búsqueda avanzada de Deezer (`artist:"..." track:"..."`) y se tomaba el primer resultado sin comprobarlo. Solo devolvió resultados para 12 de 1.522 canciones, y los 12 eran incorrectos (casi todos la misma canción, «Rolling 200 Deep», que acredita a cientos de artistas). Por eso se pasó a la búsqueda normal y se añadió la comprobación del título.
4. **Detalles:** con los identificadores del resultado elegido se piden los datos del álbum (`/album/{id}`) y del artista (`/artist/{id}`).
5. **Límite de peticiones:** se espera 0,2 s entre peticiones (5 por segundo, por debajo de 50 cada 5 segundos).
6. **Salida (datos originales, no se modifican después):**
   - `data/raw/deezer_respuestas_originales.json`: todas las respuestas de la API tal cual;
   - `data/raw/deezer_canciones.csv`: una fila por canción con los campos de la tabla anterior.
7. **Preparación** (`api/dataframe_api.py`): se cargan los datos en un DataFrame, se revisan tipos, nulos y duplicados, se marcan las coincidencias incorrectas (karaoke, covers, tributos u otra canción) en la columna `coincidencia_correcta` y se vacían sus datos de Deezer. Resultado en `data/processed/deezer_canciones_preparado.csv`.
8. **Unión con el scraping:** `merge` por `titulo` + `artista`, conservando todas las filas de las listas.

**Ejecución** (desde la carpeta principal del repositorio): `python api/api_deezer.py` (unos 40 minutos) y después `python api/dataframe_api.py`.

**Herramientas:** Python 3, `requests` y `pandas`.

---

## 6. robots.txt y condiciones de uso

- **robots.txt de `api.deezer.com`:** contiene `User-agent: *` y `Disallow: /*`, es decir, prohíbe el rastreo de todo el dominio a los robots. Esto es habitual en las APIs: MusicBrainz bloquea `/ws` en su robots.txt y Apple bloquea `/search` y `/lookup` en el de la API de iTunes. El robots.txt está pensado para **rastreadores** (buscadores e indexadores), que siguen enlaces y descargan páginas. Una API es el **canal oficial que el propio servicio ofrece** para acceder a sus datos con programas, y su uso se rige por sus condiciones de uso. Nosotros no rastreamos el dominio: solo hacemos peticiones concretas a los endpoints documentados.
- **Condiciones de Deezer:** el uso de la API está sujeto a los *Terms of use* de Deezer for Developers. Las pautas de desarrolladores prohíben el **almacenamiento local de audio**. Nosotros **no descargamos audio**, ni siquiera los fragmentos de 30 s (`preview`): solo guardamos metadatos (textos y números).
- **Uso responsable:** las peticiones se espacian para respetar el límite, el User-Agent identifica el proyecto como académico y se usa una caché para no repetir consultas.
- **Finalidad:** uso académico y no comercial. Los datos no se redistribuyen fuera del repositorio del proyecto.

---

## 7. Limitaciones de los datos de la API

- **Los datos son de hoy, no del año de la lista:** `rank` y `nb_fan` miden la popularidad actual en Deezer. Por eso favorecen a los artistas recientes y no sirven para comparar la popularidad que tenían en 2005.
- **El sello de Deezer es el del lanzamiento en la plataforma:** puede ser una reedición o una distribuidora, como «Universal Music» en lugar del sello original. Por eso el sello de referencia es el de Official Charts, y el de Deezer solo se usa para contrastar o completar.
- **El género es del álbum, no de la canción**, y a veces viene vacío.
- **Puede haber coincidencias erróneas o canciones sin encontrar**: la búsqueda solo comprueba el título, así que puede devolver versiones karaoke, covers o tributos. En la preparación se detectaron 37 y se vaciaron sus datos. Una de ellas era correcta: «MY LOVER» de NOT3S, que Deezer atribuye a Mabel, que colabora en la canción. Tampoco se encuentran canciones cuyo título lleva signos distintos en Deezer (ET → «E.T.», SENORITA → «Señorita») ni las caras A/B que Official Charts une con `/`.
- **La fecha de lanzamiento es la del álbum en Deezer** y puede ser la de una reedición o un recopilatorio, lo que haría parecer las canciones más recientes de lo que son.

---

## 8. Resultados de la obtención

- Fecha de la consulta: 19 de noviembre de 2026
- Canciones distintas consultadas: 1.522 (de 2.100 filas del scraping)
- Encontradas en Deezer: 1.478; no encontradas: 44
- Coincidencias incorrectas detectadas en la preparación: 37
- Canciones con datos de Deezer válidos tras la preparación: 1.441 (95 %)