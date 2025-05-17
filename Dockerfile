FROM python:3.9-slim

# Crear usuario no root
RUN useradd -m -u 1000 strava_user

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements.txt primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Crear directorio results y establecer permisos
RUN mkdir -p results && \
    chown -R strava_user:strava_user /app

# Cambiar al usuario no root
USER strava_user

# Comando por defecto
CMD ["python", "-m", "unittest", "test_strava_scraper.py", "-v"] 