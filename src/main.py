import requests
from config import config
from utils import create_database, save_data_to_database_emp, save_data_to_database_vac, get_vacancies_data
from DBManager import DBManager


def main():

    company_ids = [
        '4307',
        '4787018',
        '4219',
        '5557093',
        '1579449',
        '2180',
        '1057',
        '1180',
        '208707',
        '205'
    ]

    params = config()
    data = get_vacancies_data(company_ids)
    create_database('hh', params)
    save_data_to_database_emp(data, 'hh', params)
    save_data_to_database_vac(data, 'hh', params)


def get_employers_and_vacancies(company_ids):
    base_url = "https://api.hh.ru/vacancies"
    headers = {"User-Agent": "Your-User-Agent"}
    employers_and_vacancies = []

    for company_id in company_ids:
        params = config()
        response = requests.get(base_url, headers=headers, params=params)
        data = get_vacancies_data()
        create_database('hh', params)
        save_data_to_database_emp(data, 'hh', params)
        save_data_to_database_vac(data, 'hh', params)

        if "employer" in data:
            employer = {"id": company_id, "name": data["employer"]["name"]}
        else:
            employer = {"id": company_id, "name": "Unknown"}

        if "items" in data:
            vacancies = [{"employer_id": company_id, "title": vacancy["name"], "salary": vacancy["salary"]} for vacancy
                         in data["items"]]
        else:
            vacancies = []

        employers_and_vacancies.append((employer, vacancies))

    return employers_and_vacancies


company_ids = [123, 456, 789]
employers_and_vacancies = get_employers_and_vacancies(company_ids)
print(employers_and_vacancies)
