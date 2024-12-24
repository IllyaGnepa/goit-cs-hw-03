from faker import Faker
import psycopg2
from random import choice

DB_CONFIG = {
    "dbname": "db_name",
    "user": "your_username",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}

fake = Faker()

def seed_data():
    statuses = ["new", "in progress", "completed"]

    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                # Додаємо статуси
                for status in statuses:
                    cur.execute("INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", (status,))
                
                # Додаємо користувачів
                users = []
                for _ in range(10):
                    fullname = fake.name()
                    email = fake.unique.email()
                    cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s) RETURNING id;", (fullname, email))
                    user_id = cur.fetchone()[0]
                    users.append(user_id)
                
                # Додаємо завдання
                for _ in range(30):
                    title = fake.sentence(nb_words=5)
                    description = fake.text(max_nb_chars=200)
                    status_id = choice(range(1, len(statuses) + 1))
                    user_id = choice(users)
                    cur.execute("""
                        INSERT INTO tasks (title, description, status_id, user_id)
                        VALUES (%s, %s, %s, %s)
                    """, (title, description, status_id, user_id))
                print("Дані успішно додано.")
    except Exception as e:
        print(f"Помилка: {e}")

if __name__ == "__main__":
    seed_data()