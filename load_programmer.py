import requests
import json

print("Успешно загружены модули\n")

with open('vacancies.json', 'w', encoding='utf-8') as file:
    json.dump([], file)
print("Успешно очищен файл с вакансиями\n")

def load_and_save_vacancies(company_id, type, filename):
    print("Начал запись в JSON\n")
    def get_vacancies_by_company(company_id, page=0):
        url = "https://api.hh.ru/vacancies"
        params = {  
            "employer_id": company_id,
            "page": page,
            "per_page": 30,
            "area": 1
        }

        response = requests.get(url, params=params).json()
        return response.get("items", [])

    vacancies_data = []
    for _ in range(1, 2):
        vacancies_info = get_vacancies_by_company(company_id, page=_)
        for item in vacancies_info:
            salary_info = item.get("salary")
            salary_from = salary_info.get("from", "Не указано") if salary_info else "Не указано"
            salary_to = salary_info.get("to", "Не указано") if salary_info else "Не указано"

            vacancy_data = {
                "type": 0,
                "name": item.get("name", ""),
                "company": item.get("employer", {}).get("name", ""),
                "salary": f"{salary_from} - {salary_to}",
                "tasks": item.get("snippet", {}).get("responsibility", ""),
                "requirements": item.get("snippet", {}).get("requirement", ""),
                "graphic": item.get("schedule", {}).get("name", ""),
                "contact": "",
                "vacancy_link": item.get("alternate_url", "")
            }
            vacancies_data.append(vacancy_data)
            print("Записал в переменную\n")

    with open(filename, "r", encoding="utf-8") as file:
        existing_data = json.load(file)

    existing_data.extend(vacancies_data)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)
        print("Успешно загружены данные\n")

load_and_save_vacancies(4826977, 1, "vacancies.json")
load_and_save_vacancies(2537115, 1, "vacancies.json")
load_and_save_vacancies(882, 1, "vacancies.json")
load_and_save_vacancies(2748, 1, "vacancies.json")
load_and_save_vacancies(2225283, 1, "vacancies.json")
load_and_save_vacancies(15478, 1, "vacancies.json")

print("Успешно загружены новые вакансии и записаны в vacancies.json")