import os
import requests
from dotenv import load_dotenv
from itertools import count
from terminaltables import AsciiTable

PROGRAMM_LANGUAGE = ["Python", "Java", "Javascript", 'C++', "C#", 'Go', 'Rust',
                     "PHP", "Ruby", "Swift", "Kotlin", "TypeScript"]


def get_hh_vacancies(language: list[str]) -> list[str]:
    """Function get list and send  GET reqeust to HeadHanter Api. Return vacancies list"""

    hh_api = "https://api.hh.ru/vacancies"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"
    }
    hh_vacancies = []
    for page in count(0):
        payload = {'professional_role': 96, 'area': '1',
                   'period': 30, 'only_with_salary': False,
                   'text': language, 'per_page': '100',
                   'page': page}

        response = requests.get(
            hh_api,  params=payload, headers=headers
        )
        response.raise_for_status()
        vacancies = response.json()
        hh_vacancies += vacancies["items"]
        if page >= vacancies["pages"] or page >= 19:
            break
    return hh_vacancies


def get_sj_vacancies(language: str, token: str) -> list:
    """Function get request to Superjob Api"""
    sjob_api = 'https://api.superjob.ru/2.0/vacancies/'
    header = {'X-Api-App-Id': token}
    sjob_vacancies = []
    for page in count(0):
        profession_category = {'33': ['36', '48', '604']}
        payload = {'town': '4', 'categories': profession_category,
                   'count': 100, 'page': page,
                   'keyword': language, 'period': 30}
        response = requests.get(sjob_api, headers=header, params=payload)
        response.raise_for_status()
        vacancies = response.json()
        sjob_vacancies += vacancies['objects']
        if not vacancies['more']:
            break
    return sjob_vacancies


def extract_hh_salary(vacancies) -> list[int]:
    """get vacancies list and return string"""
    salaries = []
    for vacancy in vacancies:
        if not vacancy["salary"]:
            continue
        salary = predict_rub_salary_for_hh(vacancy["salary"])
        if not salary:
            continue
        salaries.append(salary)
    return salaries

def extract_sj_salary(vacancies) -> list[int]:
    """get vacancies list and return string"""
    salaries = []
    for vacancy in vacancies:
        salary = predict_rub_salary_for_sj(vacancy)
        if not salary:
            continue
        salaries.append(salary)
    return salaries



def calculate_average_salary(salary_from: int, salary_to: int) -> int:
    """Func get salary_from, salary_to and return average salary"""
    average_salary = 0
    if salary_from and salary_to:
        average_salary = (salary_from + salary_to) // 2
    elif salary_from:
        average_salary = salary_from * 1.2
    elif salary_to:
        average_salary = salary_to * 0.8
    return average_salary


def predict_rub_salary_for_hh(salary: dict) -> int:
    """The function predicts the salary in rubles in HeahHunter vacancies"""
    average_salary = 0
    if salary["currency"] == "RUR":
        average_salary = calculate_average_salary(salary["from"], salary["to"])
    return average_salary

def predict_rub_salary_for_sj(vacancy: dict) -> int:
    average_salary = 0
    if vacancy["currency"] == "rub":
        average_salary = calculate_average_salary(vacancy["payment_from"], vacancy["payment_to"])
    return average_salary

def create_table(salary_by_language):
    table_salaries = [
        ["Язык программирования", "Вакансий найдено", "Вакансий обработано",
         "Средняя зарплата"]]
    for language, properties_vacancies in salary_by_language.items():
        table_salaries.append([language, properties_vacancies['vacancies_found'],
                               properties_vacancies['vacancies_processed'],
                               properties_vacancies['average_salary']])
    table = AsciiTable(table_salaries)
    table.inner_row_border = True
    return table


def combine_hh_salaries():
    salary_by_languages = {}
    for language in PROGRAMM_LANGUAGE:
        response = get_hh_vacancies(language)
        salaries = extract_hh_salary(response)
        reps_counts = len(response)
        try:
            average_salary = int(sum(salaries) / len(salaries))
        except ZeroDivisionError:
            average_salary = 0

        salary_by_languages[language] = {'vacancies_found': reps_counts,
                                         'vacancies_processed': len(salaries),
                                         'average_salary': average_salary}
    return salary_by_languages


def combine_sj_vacancies():
    salary_by_languages = {}
    for language in PROGRAMM_LANGUAGE:
        response = get_sj_vacancies(language, token)
        salaries = extract_sj_salary(response)
        reps_counts = len(response)
        try:
            average_salary = int(sum(salaries) / len(salaries))
        except ZeroDivisionError:
            average_salary = 0
        salary_by_languages[language] = {'vacancies_found': reps_counts,
                                         'vacancies_processed': len(salaries),
                                         'average_salary': average_salary}
    return salary_by_languages


if __name__ == "__main__":
    load_dotenv()

    token = os.environ['SJ_TOKEN']

    table = create_table(combine_hh_salaries())
    table.title = 'HeadHunter Moscow'
    print(table.table)
    print()

    table = create_table(combine_sj_vacancies())
    table.title = "SuperJob Moskow"
    print(table.table)

