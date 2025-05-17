from strava_scraper import StravaScraper
import argparse

def search_users(name: str):
    """
    Busca usuarios por nombre y muestra los resultados paginados.
    
    Args:
        name: Nombre a buscar
    """
    scraper = StravaScraper()
    page = 1
    total_results = 0
    
    print(f"\nBuscando usuarios con nombre: {name}")
    print("-" * 50)
    
    while True:
        print(f"\nPágina {page}:")
        print("-" * 30)
        
        try:
            results = scraper.search_users_by_name(name, page)
            
            if not results:
                if page == 1:
                    print("No se encontraron resultados.")
                break
            
            for user in results:
                print(f"ID: {user['id']}")
                print(f"Nombre: {user['name']}")
                print(f"Ubicación: {user['location']}")
                print("-" * 30)
            
            total_results += len(results)
            
            # Verificar si hay más páginas
            if not scraper.has_next_page:
                print("\nNo hay más páginas disponibles.")
                break
            
            page += 1
            
        except Exception as e:
            print(f"Error al buscar en la página {page}: {str(e)}")
            break
    
    print(f"\nTotal de usuarios encontrados: {total_results}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Buscar usuarios en Strava')
    parser.add_argument('name', help='Nombre a buscar')
    args = parser.parse_args()
    
    search_users(args.name) 