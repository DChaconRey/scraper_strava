# Strava Scraper

Un scraper para obtener información de perfiles de usuarios de Strava.

## Requisitos

- Python 3.9+
- Docker (opcional)

## Configuración

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/strava-scraper.git
cd strava-scraper
```

2. Crea un archivo `.env` con las siguientes variables:
```
_strava4_session=tu_cookie_session
sp=tu_cookie_sp
_currentH=d3d3LnN0cmF2YS5jb20=
_strava_cbv3=true
```

## Uso

### Usando Python directamente

1. Instala las dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecuta los tests:
```bash
python -m unittest test_strava_scraper.py -v
```

### Usando Docker

1. Construye la imagen:
```bash
docker build -t strava-scraper .
```

2. Ejecuta el contenedor:
```bash
docker run -v $(pwd)/.env:/app/.env -v $(pwd)/results:/app/results strava-scraper
```

## Estructura del Proyecto

- `strava_scraper.py`: Clase principal del scraper
- `test_strava_scraper.py`: Tests unitarios
- `requirements.txt`: Dependencias del proyecto
- `Dockerfile`: Configuración para Docker
- `results/`: Directorio donde se guardan los resultados

## Funcionalidades

- Búsqueda de usuarios por nombre
- Obtención de perfiles de usuario
- Extracción de información como:
  - Nombre
  - Ubicación
  - Descripción
  - URL de imagen de perfil
  - Información de actividades

## Licencia

MIT


# scraper_strava
