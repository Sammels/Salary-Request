import time
import requests
import logging

def parse_hh():
    programm_language_popular = {}
    programm_languages = ["Python", "Java", "Javascript", "Ruby",
                          "PHP", "C++", "C#", "C",
                          "Go", "Shell"]

    vacancie_url_api = 'https://api.hh.ru/vacancies'
    headers = {
        'User-Agent': 'api-test-agent'
    }

    for language in programm_languages:

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
        salary = cont[0]['salary']
        print(language, salary)

        # # Parse work title
        # vacansies_list = []
        # for number, items in enumerate(cont):
        #     print(number, items.get('name'), f"city: {items.get('area')['name']}")

        # Шаг 3 словарь с языками
        programm_language_popular[language] = found_vacancies

    print(programm_language_popular)


def predict_rub_salary(vacancies_id: str) -> str:
    """The function predicts the salary in rubles"""
    vacancies_url_api = f'https://api.hh.ru/vacancies/{vacancies_id}'

    headers = {
        'User-Agent': 'api-test-agent'
    }

    payload = {
        'area': '1',
        'period': 3,
        'only_with_salary': True,
        'currency': 'RUR',
    }
    response = requests.get(vacancies_url_api, headers=headers, params=payload)
    response.raise_for_status()
    container = response.json().get("salary")

    if 'USD' not in container['currency']:
        if not container['from']:
            max_salary = container['to'] * 0.8
            print(max_salary)
        elif not container['to']:
            min_salary = container['from'] * 1.2
            print(min_salary)
        else:
            min_salary = container['from']
            max_salary = container['to']
            current_salary = (min_salary + max_salary) // 2
            print(current_salary)
    else:
        print(None)





if __name__ == "__main__":
    start_time = time.time()

    vacancie_url_api = 'https://api.hh.ru/vacancies'

    headers = {
        'User-Agent': 'api-test-agent'
    }

    payload = {
        'area': '1',
        'per_page': 20,
        'text': "Программист Python",
        'period': 3,
        'only_with_salary': True,
        'currency': 'RUR',
    }

    response = requests.get(vacancie_url_api, headers=headers, params=payload)
    response.raise_for_status()
    cont = response.json().get('items')


    vacansies_list = []
    for number, items in enumerate(cont):
        vacancies_id = items['id']
        salary = items['salary']

        predict_rub_salary(vacancies_id)

        # print(number, items.get('name'),
        #       "Salary: ", salary,
        #       vacancies_id)


    # Check time resource
    end_time = time.time() - start_time
    print('\n', end_time)
