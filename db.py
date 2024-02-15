import csv
import sqlite3
from datetime import datetime


class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls, *args, **kwargs)
            cls._instance.conn = sqlite3.connect('dataset.sqlite', check_same_thread=False)
            cls._instance.cur = cls._instance.conn.cursor()
            cls._instance.create_table()
            cls._instance.load_data()
        return cls._instance

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS dataset (
                            category TEXT,
                            firstname TEXT,
                            lastname TEXT,
                            email TEXT,
                            gender TEXT,
                            birthDate TEXT
                        )''')
        self.conn.commit()

    def insert_data(self, data):
        self.cur.execute('''INSERT INTO dataset (category, firstname, lastname, email, gender, birthDate) 
                            VALUES (?, ?, ?, ?, ?, ?)''',
                          (data['category'], data['firstname'], data['lastname'], data['email'], data['gender'], data['birthDate']))
        self.conn.commit()

    def fetch_data(self, filters=None, limit=None, offset=None):
        sql_query = "SELECT * FROM dataset WHERE 1=1"
        if filters:
            age_range = filters.pop('age_range', None)
            age = filters.pop('age', None)
            if age_range:
                min_age, max_age = map(int, age_range.split('-'))
                current_year = datetime.now().year
                min_birth_year = current_year - max_age
                max_birth_year = current_year - min_age
                sql_query += f" AND birthDate BETWEEN {min_birth_year} AND {max_birth_year}"
            if age:
                current_year = datetime.now().year
                year = current_year - int(age)
                sql_query += f" AND strftime('%Y', birthDate) = '{year}'"
            sql_query += ''.join([f" AND {key}='{value}'" for key, value in filters.items()])
        if limit is not None:
            sql_query += f" LIMIT {limit}"
        if offset is not None:
            sql_query += f" OFFSET {offset}"
        print(sql_query)
        self.cur.execute(sql_query)
        return self.cur.fetchall()

    def fetch_dataset(self, filters=None, limit=None, offset=None):
        sql_query = "SELECT * FROM dataset WHERE 1=1"
        if filters:
            age_range = filters.pop('age_range', None)
            age = filters.pop('age', None)
            if age_range:
                min_age, max_age = map(int, age_range.split('-'))
                current_year = datetime.now().year
                min_birth_year = current_year - max_age
                max_birth_year = current_year - min_age
                sql_query += f" AND birthDate BETWEEN {min_birth_year} AND {max_birth_year}"
            if age:
                current_year = datetime.now().year
                year = current_year - int(age)
                sql_query += f" AND strftime('%Y', birthDate) = '{year}'"
            sql_query +=''.join([f" AND {key}='{value}'" for key, value in filters.items()])
        self.cur.execute(sql_query)
        return self.cur.fetchall()


    def close_connection(self):
        self.conn.close()

    def load_data(self):
        with open('data/dataset.txt') as file:
            reader = csv.DictReader(file)
            rows_to_insert = []
            for row in reader:
                rows_to_insert.append((row['category'], row['firstname'], row['lastname'], row['email'], row['gender'], row['birthDate']))

            self.cur.executemany('''INSERT INTO dataset (category, firstname, lastname, email, gender, birthDate) 
                                            VALUES (?, ?, ?, ?, ?, ?)''', rows_to_insert)
            self.conn.commit()