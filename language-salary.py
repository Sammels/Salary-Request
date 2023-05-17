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

    page = 0
    pages_number = 20

    while page < pages_number:

        for language in programm_languages:
            payload = {
                'area': '1',
                'page': page,
                'text': f"Программист {language}",
                'period': 30,
                'only_with_salary': True,
                'currency': 'RUR',
            }
            page_response = requests.get(vacancie_url_api, headers=headers, params=payload)
            page_response.raise_for_status()
            page_payload = page_response.json()
            page_items = page_payload.get('items')
            found_vacancies = page_response.json().get('found')
            pages_number = page_payload['page']
            page += 1


            for number, items in enumerate(page_items):
                programm_language = {}
                vacancies_id = items['id']
                prediction_salary = predict_rub_salary(vacancies_id)
                if prediction_salary is not None:
                    average_salary.append(prediction_salary)

                vacancies_processed.append(number)
                programm_language['found_vacancies'] = found_vacancies
                programm_language['vacancies_processed'] = len(average_salary)
                programm_language['average_salary'] = sum(average_salary) // len(average_salary)


            programm_language_popular[language] = programm_language


            print(programm_language_popular)
            average_salary = []
            time.sleep(8)

    # Check time resource
    end_time = time.time() - start_time
    print('\n', end_time)
