import psycopg2


class DBManager:
    def __init__(self, params):
        self.conn = psycopg2.connect(dbname='hh', **params)
        self.cursor = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """
        получает список всех компаний и количество вакансий у каждой компании
        """
        self.cursor.execute("""
            SELECT c.company_name, COUNT(v.vacancy_id) AS vacancy_counter 
            FROM companies c
            LEFT JOIN vacancies v USING(company_id)
            GROUP BY c.company_name;
        """)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        """
        получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """
        self.cursor.execute("""
            SELECT c.company_name, v.vacancy_name, v.salary_min, v.salary_max, v.vacancy_url
            FROM companies c
            JOIN vacancies v USING(company_id);
        """)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        """
        получает среднюю зарплату по вакансиям
        """
        self.cursor.execute("""
            SELECT ROUND(AVG((salary_min + salary_max) / 2)) AS avg_salary
            FROM vacancies;
        """)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """
        получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        self.cursor.execute("""
            SELECT * FROM vacancies
            WHERE (salary_min + salary_max) > 
            (SELECT AVG(salary_min + salary_max) FROM vacancies);
        """)
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """
        получает список всех вакансий,
        в названии которых содержатся переданные в метод слова
        """
        query = """
                SELECT * FROM vacancies
                WHERE LOWER(vacancy_name) LIKE %s
                """
        self.cursor.execute(query, ('%' + keyword.lower() + '%',))
        return self.cursor.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()
