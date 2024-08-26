import pytest
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from data_pipeline.api import get_all_characters

def test_get_all_characters_success(requests_mock):
    # Simula uma resposta bem-sucedida da API
    url = 'https://rickandmortyapi.com/api/character'
    mock_response = {"results": [{"id": 1, "name": "Rick Sanchez"}, {"id": 2, "name": "Morty Smith"}]}
    requests_mock.get(url, json=mock_response, status_code=200)

    response = get_all_characters(url)
    assert response == mock_response

def test_get_all_characters_http_error(requests_mock):
    # Simula um erro HTTP (por exemplo, 404 Not Found)
    url = 'https://rickandmortyapi.com/api/character'
    requests_mock.get(url, status_code=404)

    with pytest.raises(HTTPError):
        get_all_characters(url)

def test_get_all_characters_connection_error(requests_mock):
    # Simula um erro de conexão
    url = 'https://rickandmortyapi.com/api/character'
    requests_mock.get(url, exc=ConnectionError)

    with pytest.raises(ConnectionError):
        get_all_characters(url)

def test_get_all_characters_timeout_error(requests_mock):
    # Simula um erro de timeout
    url = 'https://rickandmortyapi.com/api/character'
    requests_mock.get(url, exc=Timeout)

    with pytest.raises(Timeout):
        get_all_characters(url)

def test_get_all_characters_request_exception(requests_mock):
    # Simula um erro de solicitação genérico
    url = 'https://rickandmortyapi.com/api/character'
    requests_mock.get(url, exc=RequestException)

    with pytest.raises(RequestException):
        get_all_characters(url)
