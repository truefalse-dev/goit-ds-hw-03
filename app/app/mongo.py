from dotenv import load_dotenv
from app.core.db import DbConnection
from app.classes.transactions import Transactions
import json

load_dotenv()

def main():
    client = DbConnection().client
    db = client.book

    db.cats.insert_many(get_from('app/cats.json'))

    print("Реалізуйте функцію для виведення всіх записів із колекції.")
    Transactions(db.cats).showAll()

    print("\nРеалізуйте функцію, яка дозволяє користувачеві ввести ім'я кота та виводить інформацію про цього кота.")
    Transactions(db.cats).showOne('Grey')

    print("\nСтворіть функцію, яка дозволяє користувачеві оновити вік кота за ім'ям.")
    Transactions(db.cats).updateOne('Grey', {"age": 7})

    print("\nСтворіть функцію, яка дозволяє додати нову характеристику до списку features кота за ім'ям.")
    Transactions(db.cats).addFeature('Grey', "active")

    print("\nРеалізуйте функцію для видалення запису з колекції за ім'ям тварини.")
    Transactions(db.cats).deleteOne('Grey')

    print("\nРеалізуйте функцію для видалення всіх записів із колекції.")
    Transactions(db.cats).deleteAll()
    Transactions(db.cats).showAll()

def get_from(file):
    f = open(file)

    # returns JSON object as 
    # a dictionary
    data = json.load(f)

    # Closing file
    f.close()

    return data

if __name__ == '__main__':
    main()