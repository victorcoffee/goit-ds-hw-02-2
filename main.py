# Модуль 2. Завдання 2

import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi

os.system("cls")

uri = "mongodb+srv://setoftest:zleWRqUfrWAV1GBP@cluster0.tquohbk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi("1"))
db = client.goit_ds_02


# Перевірка зв'язку з базою
def test_connection():
    try:
        client.admin.command("ping")
        print("Ви успішно з'єдналися з MongoDB!")
        print("Поточна база: ", db.name)
    except Exception as e:
        print("Помилка підключення до бази даних", e)
        raise SystemExit


# Виведення відомостей про всіх котів
def display_all():
    print("Всі наші коти:")
    result = db.cats.find({})
    for el in result:
        print(el)


# Пошук кота за ім'ям
def find():
    name = input("Введіть ім'я кота: ")
    result = db.cats.find_one({"name": name})
    if result:
        print(result)
    else:
        print(f"В базі відсутні відомості про {name}")


# Додавання нового кота
def add():
    name = input("Введіть ім'я кота: ")
    if not name:
        print(f"У кота має бути ім'я")
    else:
        try:
            age = int(input("Вік кота: "))
            if age < 0:
                raise ValueError
            features = []
            feature = input("Особливості кота: ")
            while feature:
                features.append(feature)
                feature = input("Чи є ще особливості? \nДля виходу натисніть Enter: ")

            result_one = db.cats.insert_one(
                {
                    "name": name,
                    "age": age,
                    "features": features,
                }
            )
            print(f"{name} додано у базу, id={result_one.inserted_id}")
        except ValueError:
            print(f"Вік кота має бути цілим невід'ємним числом")


# Додавання нових ознак кота
def add_feature():
    name = input("Введіть ім'я кота: ")
    cat = db.cats.find_one({"name": name})
    if cat:
        feature = input("Введіть характеристику кота: ")
        if feature not in cat["features"]:
            db.cats.update_one({"name": name}, {"$push": {"features": feature}})
            result = db.cats.find_one({"name": name})
            print("Запис оновлено")
            print(result)
        else:
            print("Така ознака вже є")
    else:
        print(f"Запис про {name} відсутній")


# Зміна віку кота
def change_age():
    name = input("Введіть ім'я кота: ")
    if db.cats.find_one({"name": name}):
        try:
            new_age = int(input("Введіть вік кота: "))
            if new_age < 0:
                raise ValueError
            db.cats.update_one({"name": name}, {"$set": {"age": new_age}})
            result = db.cats.find_one({"name": name})
            print("Запис оновлено")
            print(result)
        except ValueError:
            print(f"Вік кота має бути цілим невід'ємним числом")
    else:
        print(f"Запис про {name} відсутній")


# Видалення кота за іменем
def delete():
    name = input("Введіть ім'я кота: ")
    result = db.cats.find_one({"name": name})
    if result:
        db.cats.delete_one({"name": name})
        print(f"Запис {name} видалено")
    else:
        print(f"Запис про {name} відсутній")


# видалення всіх записів із колекції
def delete_all():
    confirm = input("Ви впевненні, що хочете видалити всі записи? так/ні \n")
    if confirm.lower() == "так":
        db.cats.delete_many({})
        print("Всі записи видалено")
    else:
        print("Останню дію скасовано")


# Виведення команд
def menu():
    print(
        """Оберіть потрібну дію:
    1 - виведення всіх записів із колекції
    2 - інформація про кота
    3 - додати нового кота
    4 - оновити вік кота
    5 - додати нову характеристику кота
    6 - видалення запису з колекції
    7 - видалення всіх записів із колекції
    8, exit - вихід"""
    )


def main():
    test_connection()
    menu()
    while True:
        print(">>>", end="")
        command = input()
        match command:
            case "1":
                display_all()
            case "2":
                find()
            case "3":
                add()
            case "4":
                change_age()
            case "5":
                add_feature()
            case "6":
                delete()
            case "7":
                delete_all()
            case "8":
                print("Сеанс роботи з базою завершено")
                break
            case "exit":
                print("Сеанс роботи з базою завершено")
                break
            case _:
                print(f"Команда {command} відсутня")

    client.close()


if __name__ == "__main__":
    main()
