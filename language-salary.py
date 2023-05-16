import time
import requests


def predict_rub_salary(vacancies_id: str) -> int:
    """The function predicts the salary in rubles"""
    vacancies_url_api = f'https://api.hh.ru/vacancies/{vacancies_id}'

    headers = {
        'User-Agent': 'api-test-agent'
    }

    payload = {
        'area': '1',
        'only_with_salary': True,
        'currency': 'RUR',
    }
    response = requests.get(vacancies_url_api, headers=headers, params=payload)
    response.raise_for_status()
    container = response.json().get("salary")

    if 'USD' not in container['currency']:
        if not container['from']:
            max_salary = int(container['to'] * 0.8)
            return max_salary
        elif not container['to']:
            min_salary = int(container['from'] * 1.2)
            return min_salary
        else:
            min_salary = container['from']
            max_salary = container['to']
            current_salary = (min_salary + max_salary) // 2
            return current_salary
    else:
        return None


if __name__ == "__main__":
    start_time = time.time()

    programm_language_popular = {}
    average_salary = []
    vacancies_processed = []

    programm_languages = ["Python", "Java", "Javascript"]

    vacancie_url_api = 'https://api.hh.ru/vacancies'

    headers = {
        'User-Agent': 'api-agent'
    }

    for language in programm_languages:
        payload = {
            'area': '1',
            'text': f"Программист {language}",
            'period': 30,
            'only_with_salary': True,
            'currency': 'RUR',
        }
        response = requests.get(vacancie_url_api, headers=headers, params=payload)
        response.raise_for_status()
        cont = response.json().get('items')
        found_vacancies = response.json().get('found')


        for number, items in enumerate(cont):
            programm_language = {}
            vacancies_id = items['id']
            prediction_salary = predict_rub_salary(vacancies_id)
            average_salary.append(prediction_salary)

            vacancies_processed.append(number)
            programm_language['found_vacancies'] = found_vacancies
            programm_language['vacancies_processed'] = len(vacancies_processed)

        vacancies_processed = []
        programm_language_popular[language] = programm_language
        #print(sum(average_salary) // len(average_salary))
        print(programm_language_popular)

        time.sleep(8)
    # Check time resource
    end_time = time.time() - start_time
    print('\n', end_time)
