import time
import requests


if __name__ == "__main__":
    start_time = time.time()
    vacancie_url_api = 'https://api.hh.ru/vacancies'
    headers = {
        'User-Agent': 'api-test-agent'
    }
    payload = {
        'area': '1',
        'text': 'Программист',
        'period': 30,
    }

    # Vacansies and Moskow
    response = requests.get(vacancie_url_api, headers=headers, params=payload)
    response.raise_for_status()
    cont = response.json().get('items')

    # Parse work title
    vacansies_list = []
    for number, items in enumerate(cont):
        print(number, items.get('name'), f"city: {items.get('area')['name']}")



    # Check time resource
    end_time = time.time() - start_time
    print('\n', end_time)
