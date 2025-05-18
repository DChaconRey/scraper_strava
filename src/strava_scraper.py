import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from typing import List, Dict, Optional
import unicodedata


class StravaScraper:
    """
    Clase para realizar web scraping de perfiles de Strava.
    """
    def __init__(self):
        """
        Inicializa el scraper con la configuración necesaria.
        """
        load_dotenv()
        self.session = requests.Session()
        self.base_url = "https://www.strava.com"
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'es-ES,es;q=0.9',
            'referer': 'https://www.strava.com/onboarding',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
        }
        self.has_next_page = False
        self._setup_session()

    def _setup_session(self):
        """
        Configura la sesión con las cookies necesarias.
        """
        # Configurar las cookies esenciales desde el archivo .env
        cookies = {
            '_strava4_session': os.getenv('_strava4_session', ''),
            '_currentH': os.getenv('_currentH', 'd3d3LnN0cmF2YS5jb20=')
        }
        
        # La cookie más importante es _strava4_session
        if not cookies['_strava4_session']:
            raise ValueError("Se requiere la variable de entorno _strava4_session")
        
        # Configurar todas las cookies en la sesión
        for name, value in cookies.items():
            self.session.cookies.set(name, value)



    ###################### 1º punto ######################

    def get_user_profile(self, user_id: str) -> Dict:
        """
        Obtiene la información del perfil de un usuario específico
        """
        url = f"{self.base_url}/athletes/{user_id}"
        response = self.session.get(url, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f"Error al acceder al perfil: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')

        profile_data = {
            "id": user_id,
            "name": self._extract_name(soup),
            "location": self._extract_location(soup),
            "description": self._extract_description(soup),
            "image_url": self._extract_image_url(soup)
        }
        
        return profile_data


    ###################### 2º punto ######################

    def search_users_by_name(self, name: str, page: int = 1) -> List[Dict]:
        """
        Busca usuarios por nombre.
        
        Args:
            name: Nombre a buscar
            page: Número de página para paginación
            
        Returns:
            Lista de usuarios encontrados con sus IDs
        """
        url = f"{self.base_url}/athletes/search"
        params = {
            'utf8': '✓',
            'text': name,
            'gsf': '1',
            'page': page
        }
        
        all_results = []
        self.has_next_page = True
        
        while self.has_next_page:
            response = self.session.get(url, params=params, headers=self.headers)
            
            if response.status_code != 200:
                raise Exception(f"Error en la búsqueda: {response.status_code}")
            
            soup = BeautifulSoup(response.text, 'html.parser')

            # Obtener resultados de la página actual
            page_results = self._parse_search_results(soup)
            all_results.extend(page_results)

            # Verificar si siguiente página
            pagination = soup.find('ul', class_='pagination')
            if pagination:
                next_page = pagination.find('li', class_='next_page')
                self.has_next_page = next_page is not None and 'disabled' not in next_page.get('class', [])
            else:
                self.has_next_page = False
            
            if self.has_next_page:
                page += 1
                params['page'] = page
        
        return all_results

    def _extract_name(self, soup: BeautifulSoup) -> str:
        """Extrae el nombre del usuario del HTML."""
        name_element = soup.find('h1', class_='athlete-name')
        return name_element.text.strip() if name_element else ""

    def _extract_location(self, soup: BeautifulSoup) -> str:
        """Extrae la ubicación del usuario del HTML."""
        location_element = soup.find('div', class_='location')
        return location_element.text.strip() if location_element else ""

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extrae la información de actividades del usuario del HTML."""
        activity_info = {}
        
        # Extraer el rango de fechas
        date_range = soup.find('div', id='interval-date-range')
        if date_range:
            activity_info['date_range'] = date_range.find('div', class_='selection').text.strip()
        
        # Extraer los totales
        totals = soup.find('ul', id='totals')
        if totals:
            total_items = totals.find_all('li')
            if len(total_items) >= 3:
                activity_info['distance'] = total_items[0].text.strip()
                activity_info['time'] = total_items[1].text.strip()
                activity_info['elevation'] = total_items[2].text.strip()
        
        # Extraer el tipo de gráfico seleccionado
        chart_type = soup.find('a', class_='button btn-xs selected')
        if chart_type:
            activity_info['chart_type'] = chart_type.text.strip()
        
        return str(activity_info)

    def _extract_image_url(self, soup: BeautifulSoup) -> str:
        """Extrae la URL de la imagen del perfil del HTML."""
        image_element = soup.find('img', class_='avatar-img')
        return image_element.get('src', '') if image_element else ""

    def _parse_search_results(self, soup: BeautifulSoup) -> List[Dict]:
        """Parsea los resultados de búsqueda del HTML."""
        results = []
        # Buscar la lista de resultados
        search_list = soup.find('ul', class_='athlete-search')
        if not search_list:
            return results
            
        # Iterar sobre cada fila de resultados
        for row in search_list.find_all('li', class_='row'):
            athlete_link = row.find('a', class_='athlete-name-link')
            if not athlete_link:
                continue
                
            user_id = athlete_link.get('data-athlete-id')
            if not user_id:
                continue

            name = athlete_link.text.strip()
            results.append({
                "id": user_id,
                "name": name,
            })
        
        return results

    def save_in_json(self, results: Dict) -> None:
        """
        Guarda los resultados en JSON
        """
        try:
            os.makedirs('results', exist_ok=True)
            file_path = os.path.join('results', 'strava_results.json')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            print(f"\nResultados guardados en {file_path}")
            
        except Exception as e:
            print(f"Error al guardar los resultados: {str(e)}")
            raise