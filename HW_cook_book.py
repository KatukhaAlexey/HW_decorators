import os
import pprint
from main import logger

path = os.path.join(os.getcwd(), 'recipes.txt')
with open(path, encoding='utf-8') as f:
    cook_book = {}
    for line in f:  # Перебераем все строки в файле
        dish = line.strip()  # Название блюда
        kol_of_ing = int(f.readline().strip())  # Ниже строка с количеством ингредиентов
        lst_of_ing = []  # Объявляем список для всех ингредиентов
        for i in range(kol_of_ing):  # Проходим далее количество строк, указанных под названием блюда
            ing, q, m = f.readline().strip().split('|')  # переменным присваиваем значения из строки по разделителю |
            lst_of_ing.append({'ingredient_name': ing, 'quantity': int(q), 'measure': m})  # добавляем ингредиенты
        cook_book[dish] = lst_of_ing  # ключу (названию блюда) указываем значение (список ингредиентов
        f.readline()  # Пустая строка
pprint.pprint(cook_book, width=100)
print()

@logger('list_of_ingredients.txt')
def get_shop_list_by_dishes(dishes_in_lst: list, person_count: int) -> dict:
    ingredients_for_cook = {}  # Инициируем список ингредиентов
    for name in dishes_in_lst:
        if name in cook_book:  # Если блюдо есть в списке блюд, то заполняем словарь
            for j in range(len(cook_book[name])):
                ingredients_for_cook.update({cook_book[name][j]['ingredient_name']:
                                             {'measure': cook_book[name][j]['measure'],
                                              'quantity': cook_book[name][j]['quantity'] * person_count}})
        else:
            continue
    return ingredients_for_cook


dishes = ['Омлет', 'Утка по-пекински']
pprint.pprint(get_shop_list_by_dishes(dishes, 2))
print()

# Должен создаться список только для Фахитос

dishes = ['Фахитос', 'Суши']
pprint.pprint(get_shop_list_by_dishes(dishes, 3))
