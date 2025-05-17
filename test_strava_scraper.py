import unittest
import os
import json
from strava_scraper import StravaScraper
from dotenv import load_dotenv

class TestStravaScraper(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada test."""
        load_dotenv()
        
        # Verificar que las cookies necesarias estén presentes
        required_cookies = ['_strava4_session', 'sp', '_currentH', '_strava_cbv3']
        missing_cookies = [cookie for cookie in required_cookies if not os.getenv(cookie)]
        
        if missing_cookies:
            self.skipTest(f"Faltan las siguientes cookies en el archivo .env: {', '.join(missing_cookies)}")
        
        self.scraper = StravaScraper()
        self.test_user_ids = ["168314352", "168314028"]
        self.test_search_name = "laura+chacon"

        os.makedirs('results', exist_ok=True)

    def test_get_users_profiles(self):
        """Test para obtener múltiples perfiles de usuario."""
        profiles = []
        for id_user in self.test_user_ids:
            profile = self.scraper.get_user_profile(id_user)
            profiles.append(profile)
        self.scraper.save_in_json({"profiles": profiles})

    def test_search_users_by_name(self):
        results = self.scraper.search_users_by_name(self.test_search_name)

        self.scraper.save_in_json({"search_results": results})

if __name__ == '__main__':
    unittest.main() 