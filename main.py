import os
from dotenv import load_dotenv
from src.strava_scraper import StravaScraper

def main():
    # Cargar variables de entorno
    load_dotenv()
    
    # Verificar que las cookies necesarias estén presentes
    required_cookies = ['_strava4_session', '_currentH']
    missing_cookies = [cookie for cookie in required_cookies if not os.getenv(cookie)]
    
    if missing_cookies:
        print(f"Error: Faltan las siguientes cookies en el archivo .env: {', '.join(missing_cookies)}")
        return
    
    try:
        scraper = StravaScraper()
        
        # Ejemplo de búsqueda de usuarios
        search_results = scraper.search_users_by_name("laura chacon")
        
        if search_results:
            # Si encontramos usuarios, obtener el perfil del primero
            first_user = search_results[0]
            profile = scraper.get_user_profile(first_user['id'])
            
            # Guardar tanto la búsqueda como el perfil
            results = {
                "search_results": search_results,
                "profile_example": profile
            }
            scraper.save_in_json(results)
            print("Búsqueda completada con éxito.")
        else:
            print("No se encontraron usuarios.")
            
    except ValueError as e:
        print(f"Error de configuración: {str(e)}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    main() 