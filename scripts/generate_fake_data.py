import os
from dotenv import load_dotenv
from faker import Faker
import pyodbc

load_dotenv()

DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

fake = Faker()
conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={DB_SERVER};DATABASE={DB_NAME};"
    f"UID={DB_USER};PWD={DB_PASSWORD};TrustServerCertificate=yes"
)
cursor = conn.cursor()

for i in range(1, 1001):
    cursor.execute(
        "INSERT INTO customers (id, full_name, registration_date, amount) VALUES (?, ?, ?, ?)",
        i, fake.name(), fake.date_this_year(), round(fake.random_number(digits=4) / 100, 2)
    )

conn.commit()
print("1000 registros insertados en customers")
