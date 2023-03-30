# Django-shop

__Задача:__ 

Напишите программу, которая выводит n первых элементов последовательности 122333444455555… 
(число повторяется столько раз, чему оно равно).

__Решение:__
```Python
def n_first_elem(n):
    temp = 0
    count = 1
    for i in range(1, n + 1):
        while temp != i and count < n + 1:
            print(i)
            temp += 1
            count += 1
        temp = 0
```

Django-проект API для магазина продуктов

### Доступная функциональность:

* Создание, редактирование, удаление категорий и подкатегорий товаров в админке.
* Подкатегории связаны с родительской категорией.
* Добавление, изменение, удаление продуктов в админке.
* Продукты относятся к определенной подкатегории и соответственно категории.
* Эндпоинты: 
  * GET http://127.0.0.1:8000/api/categories/ - просмотр всех категорий 
  с подкатегориями (предусмотрена пагинация);
  * GET http://127.0.0.1:8000/api/products/ - просмотр всех продуктов 
  (предусмотрена пагинация);
  * GET http://127.0.0.1:8000/api/cart/{id}/ - просмотр состава корзины с 
  подсчетом количества товаров и суммы стоимости товаров в корзине;
    * POST http://127.0.0.1:8000/api/cart/{id}/cart_item/ - добавление 
    нового товара в корзину;
    * PATCH http://127.0.0.1:8000/api/cart/{id}/cart_item/ - изменение количества товара. 
    Обязательный параметр: 
      * count - количество ("-" если необходимо убавить количество, при уменьшении 
      количеств продукта до 0 - продукт удаляется из корзины));
    * DELETE http://127.0.0.1:8000/api/cart/{id}/cart_item/ - полная отчистка корзины.
* Эндпоинты для регистрации и авторизации:
  * http://127.0.0.1:8000/api/auth/users/ - регистрация нового пользователя. 
  Обязательные параметры: 
    * username
    * password
  * http://127.0.0.1:8000/api/auth/jwt/create/ - создание JWT-токена. 
  Обязательные параметры: 
    * username
    * password

### Использованные инструменты:

* Python
* Django REST Framework
* JWT + Djoser

### Установка и запуск

1. Клонировать проект, создать и активировать виртуальное окружение, установить
зависимости

Для Windows:

```shell
git clone git@github.com:elityaev/Django-shop.git
cd Django-shop
python -m venv venv
venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
Для Linux:

```shell
git clone git@github.com:elityaev/Django-shop.git
cd Django-shop
python3 -m venv venv
source venv/bin/activat
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
2. Перейти в папку ```/src```, применить миграции 
```shell
cd src
python manage.py migrate
```
3. Создать суперпользователя и через админку заполнить БД (категории, подкатегории, продукты)
```shell
python manage.py createsuperuser
```
4. Запустить проект
```shell
python manage.py runserver
```
### Документация к API:

http://127.0.0.1:8000/swagger/

http://127.0.0.1:8000/redoc/

----
_Автор Литяев Евгений_

    
