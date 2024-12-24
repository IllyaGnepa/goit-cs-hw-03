from pymongo import MongoClient
from bson.objectid import ObjectId

# Підключення до MongoDB
def connect_to_mongo():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["cats_db"]
        collection = db["cats"]
        return collection
    except Exception as e:
        print(f"Помилка підключення до MongoDB: {e}")
        return None

# Функція для створення запису
def create_cat(collection, name, age, features):
    try:
        document = {"name": name, "age": age, "features": features}
        collection.insert_one(document)
        print(f"Кіт {name} успішно доданий.")
    except Exception as e:
        print(f"Помилка створення запису: {e}")

# Функція для читання всіх записів
def read_all_cats(collection):
    try:
        for cat in collection.find():
            print(cat)
    except Exception as e:
        print(f"Помилка читання записів: {e}")

# Функція для читання запису за ім'ям
def read_cat_by_name(collection, name):
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"Кота з ім'ям {name} не знайдено.")
    except Exception as e:
        print(f"Помилка читання запису: {e}")

# Функція для оновлення віку кота за ім'ям
def update_cat_age(collection, name, new_age):
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.modified_count > 0:
            print(f"Вік кота {name} успішно оновлений.")
        else:
            print(f"Кота з ім'ям {name} не знайдено.")
    except Exception as e:
        print(f"Помилка оновлення віку: {e}")

# Функція для додавання нової характеристики
def add_feature_to_cat(collection, name, feature):
    try:
        result = collection.update_one({"name": name}, {"$addToSet": {"features": feature}})
        if result.modified_count > 0:
            print(f"Характеристика '{feature}' успішно додана для кота {name}.")
        else:
            print(f"Кота з ім'ям {name} не знайдено.")
    except Exception as e:
        print(f"Помилка додавання характеристики: {e}")

# Функція для видалення запису за ім'ям
def delete_cat_by_name(collection, name):
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Кіт {name} успішно видалений.")
        else:
            print(f"Кота з ім'ям {name} не знайдено.")
    except Exception as e:
        print(f"Помилка видалення запису: {e}")

# Функція для видалення всіх записів
def delete_all_cats(collection):
    try:
        collection.delete_many({})
        print("Усі записи успішно видалені.")
    except Exception as e:
        print(f"Помилка видалення всіх записів: {e}")

# Основна функція
def main():
    collection = connect_to_mongo()
    if collection is None:
        return
    
    while True:
        print("\nОперації з MongoDB:")
        print("1. Додати кота")
        print("2. Показати всіх котів")
        print("3. Знайти кота за ім'ям")
        print("4. Оновити вік кота")
        print("5. Додати характеристику коту")
        print("6. Видалити кота за ім'ям")
        print("7. Видалити всіх котів")
        print("8. Вийти")
        
        choice = input("Оберіть операцію (1-8): ")
        
        if choice == "1":
            name = input("Введіть ім'я кота: ")
            age = int(input("Введіть вік кота: "))
            features = input("Введіть характеристики через кому: ").split(", ")
            create_cat(collection, name, age, features)
        elif choice == "2":
            read_all_cats(collection)
        elif choice == "3":
            name = input("Введіть ім'я кота: ")
            read_cat_by_name(collection, name)
        elif choice == "4":
            name = input("Введіть ім'я кота: ")
            new_age = int(input("Введіть новий вік кота: "))
            update_cat_age(collection, name, new_age)
        elif choice == "5":
            name = input("Введіть ім'я кота: ")
            feature = input("Введіть нову характеристику: ")
            add_feature_to_cat(collection, name, feature)
        elif choice == "6":
            name = input("Введіть ім'я кота: ")
            delete_cat_by_name(collection, name)
        elif choice == "7":
            delete_all_cats(collection)
        elif choice == "8":
            print("Вихід.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()