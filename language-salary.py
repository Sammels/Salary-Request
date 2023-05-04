import time
import requests


if __name__ == "__main__":
    programm_language_popular = {}
    start_time = time.time()
    programm_language = ["Python", "Java", "Javascript", "Ruby",
                         "PHP", "C++"]

    vacancie_url_api = 'https://api.hh.ru/vacancies'
    headers = {
        'User-Agent': 'api-test-agent'
    }
    for language in programm_language:

        payload = {
            'area': '1',
            'text': f"Программист {language}",
            'period': 30,
            'only_with_salary': True,
        }


        # Vacansies in Moskow
        response = requests.get(vacancie_url_api, headers=headers, params=payload)
        response.raise_for_status()
        cont = response.json().get('items')
        found_vacancies = response.json().get('found')

        # # Parse work title
        # vacansies_list = []
        # for number, items in enumerate(cont):
        #     print(number, items.get('name'), f"city: {items.get('area')['name']}")

        # Шаг 3 словарь с языками
        programm_language_popular = {f"{language}": found_vacancies}

        print(programm_language_popular)

    # Check time resource
    end_time = time.time() - start_time
    print('\n', end_time)
