import time
import requests


def predict_rub_salary(vacancies_id: str) -> int:
    """The function predicts the salary in rubles"""
    container = vacancies_id

    if "USD" not in container["currency"]:
        if not container["from"]:
            max_salary = int(container["to"] * 0.8)
            return max_salary
        elif not container["to"]:
            min_salary = int(container["from"] * 1.2)
            return min_salary
        else:
            min_salary = container["from"]
            max_salary = container["to"]
            current_salary = (min_salary + max_salary) // 2
            return current_salary
    else:
        return None


if __name__ == "__main__":
    start_time = time.time()

    programm_language_popular = {}
    average_salary = []
    vacancies_processed = []

    massive_data = []

    #programm_languages = ["Python", "Java", "Javascript"]
    programm_languages = ["Python",]

    vacancie_url_api = "https://api.hh.ru/vacancies"

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"}

    page = 0
    pages_number = 20

    while page < pages_number:
        for language in programm_languages:
            payload = {
                "area": "1",
                "page": page,
                "text": f"{language} разработчик",
                "period": 30,
                "only_with_salary": True,
                "currency": "RUR",
            }
            page_response = requests.get(
                vacancie_url_api, headers=headers, params=payload
            )
            page += 1
            page_response.raise_for_status()
            page_payload = page_response.json()
            page_items = page_payload.get("items")
            found_vacancies = page_response.json().get("found")


            for number, items in enumerate(page_items):
                avenue = items.get("salary")
                summary = predict_rub_salary(avenue)
                if massive_data is not None:
                    massive_data.append(summary)
                print(language, massive_data)

            print(massive_data)



    # Check time resource
    end_time = time.time() - start_time
    print("\n", end_time)
