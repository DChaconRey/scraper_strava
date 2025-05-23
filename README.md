# Strava Web Scraper

Scraper para Strava que permite extraer información de perfiles de usuario y realizar búsquedas.

## Requisitos Previos

- Python 3.9+
- pip (gestor de paquetes de Python)

## Instalación

1. Clona el repositorio:
```bash
git clone <url-del-repositorio>
cd strava
```

2. Crea un entorno virtual (recomendado):
```bash
python -m venv venv
# En Windows:
.\venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Configuración

1. Copia el archivo de ejemplo de variables de entorno:
```bash
cp .env
```

2. Edita el archivo `.env` y configura las siguientes cookies:
```
_strava4_session=tu_cookie_session
sp=tu_cookie_sp
_currentH=tu_cookie_currentH
_strava_cbv3=tu_cookie_cbv3
```

> **Nota**: Estas cookies son necesarias para la autenticación con Strava. Puedes obtenerlas iniciando sesión en Strava desde tu navegador y copiando las cookies desde las herramientas de desarrollo (F12 > Application > Cookies).

## Uso
En los test encontramos las dos tareas a hacer: 
  - La busqueda de un usuario especifico dado el id 
  - La busqueda todos los usuarios dados un nombre.

En el main hacemos un mix y ejecutamos la busqueda de todos los usuarios dados un nombre y nos quedamos con el primer
resultado 

### Ejecutar el Scraper

Para ejecutar el scraper principal:
```bash
python main.py
```

### Ejecutar los Tests

Para ejecutar los tests:
```bash
python -m pytest tests/
```

## Estructura del Proyecto

```
├── src/               # Código fuente
│   └── strava_scraper.py
├── tests/            # Tests
│   └── test_strava_scraper.py
├── .env.example      # Ejemplo de variables de entorno
├── .env             # Variables de entorno (no incluir en git)
├── requirements.txt  # Dependencias
└── main.py          # Punto de entrada
```

## Licencia

MIT