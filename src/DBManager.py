import psycopg2


class DBManager:
    def __init__(self, params):
        self.conn = psycopg2.connect(dbname='hh', **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        self.cursor.execute("""
            SELECT c.name, COUNT(v.id) as vacancies_count
            FROM companies c
            JOIN vacancies v ON c.id = v.company_id
            GROUP BY c.id
        """)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        self.cursor.execute("""
            SELECT c.name, v.title, v.salary, v.link
            FROM companies c
            JOIN vacancies v ON c.id = v.company_id
        """)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        self.cursor.execute("""
            SELECT AVG(salary) FROM vacancies
        """)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        self.cursor.execute("""
            SELECT c.name, v.title, v.salary, v.link
            FROM companies c
            JOIN vacancies v ON c.id = v.company_id
            WHERE v.salary > %s
        """, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        self.cursor.execute("""
            SELECT c.name, v.title, v.salary, v.link
            FROM companies c
            JOIN vacancies v ON c.id = v.company_id
            WHERE v.title ILIKE %s
        """, ('%' + keyword + '%',))
        return self.cursor.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()
