import requests

def get_all_characters(url='https://rickandmortyapi.com/api/character'):
    """
    Retorna a resposta da API Rick and Morty.
    
    Parameters:
        url (str): URL da API. Padrão é a URL de todos os personagens.
    
    Returns:
        response (requests.Response): Objeto de resposta da solicitação HTTP.
    """
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}") # Exemplo: 404 Not Found
        raise
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}") # Exemplo: Failed to establish a new connection
        raise
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}") # Exemplo: Request timed out
        raise
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}") # Exemplo: Too many redirects
        raise
