'''Цель: выработать навык работы с CRUD запросами.

Задача "Имитация работы с БД":
Создайте новое приложение FastAPI и сделайте CRUD запросы.
Создайте словарь users = {'1': 'Имя: Example, возраст: 18'}
Реализуйте 4 CRUD запроса:
get запрос по маршруту '/users', который возвращает словарь users.
post запрос по маршруту '/user/{username}/{age}', который добавляет в словарь по максимальному по значению
ключом значение строки "Имя: {username}, возраст: {age}". И возвращает строку "User <user_id> is registered".
put запрос по маршруту '/user/{user_id}/{username}/{age}', который обновляет значение из словаря users под
ключом user_id на строку "Имя: {username}, возраст: {age}". И возвращает строку "The user <user_id> is updated"
delete запрос по маршруту '/user/{user_id}', который удаляет из словаря users по ключу user_id пару.
'''
from fastapi import FastAPI, Path
from typing import Annotated
import uvicorn

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}

def _max_user_id_as_int():
    return int(max(users, key=int))
@app.get('/users')
async def get_users() -> dict:
    return users

@app.post('/user/{username}/{age}')
async def post_user(username: Annotated[str, Path(min_length=3, max_length=15, description='Введите имя_пользователя', example='OldGoodUser')],
                    age: Annotated[int, Path(ge=18, le=120, description='Введите Ваш возраст', example='39')]) -> str:
    user_id = _max_user_id_as_int() + 1
    users[str(user_id)] = f'Имя: {username}, возраст: {age}'
    return f'User with user_id {user_id} is registered.'

@app.put('/user/{user_id}/{username}/{age}')
async def post_user(user_id: Annotated[int, Path(ge=1, le=999, description='Введите user_id (целое число)', example=10)],
                    username: Annotated[str, Path(min_length=3, max_length=15, description='Введите имя_пользователя', example='UrbanUser')],
                    age: Annotated[int, Path(ge=18, le=120, description='Введите Ваш возраст', example='39')]) -> str:
    if user_id <= _max_user_id_as_int():
        users[str(user_id)] = f'Имя: {username}, возраст: {age}'
        return f'The user with user_id {user_id} is updated.'
    else:
        return f'The user with user_id {user_id} was not found. Please, try user_id < {_max_user_id_as_int() + 1}'

@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=1, le=_max_user_id_as_int(), description='Введите user_id (целое число)', example=_max_user_id_as_int())]) -> str:
    users.pop(str(user_id))
    return f'The user with user_id {user_id} was deleted.'

@app.get('/')
async def main() -> str:
    return 'Перейдите на страницу http://127.0.0.1:7000/docs'

'''
Выполните каждый из этих запросов по порядку. Ответы должны совпадать:
1. GET '/users'
{
"1": "Имя: Example, возраст: 18"
}
2. POST '/user/{username}/{age}' # username - UrbanUser, age - 24
"User 2 is registered"
3. POST '/user/{username}/{age}' # username - NewUser, age - 22
"User 3 is registered"
4. PUT '/user/{user_id}/{username}/{age}' # user_id - 1, username - UrbanProfi, age - 28
"User 1 has been updated"
5. DELETE '/user/{user_id}' # user_id - 2
"User 2 has been deleted"
6. GET '/users'
{
"1": "Имя: UrbanProfi, возраст: 28",
"3": "Имя: NewUser, возраст: 22"
}
Пример результата выполнения программы:
Как должен выглядеть Swagger...
Примечания:
Не забудьте написать валидацию для каждого запроса, аналогично предыдущему заданию.'''

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=7000, log_level='info')
    # https://127.0.0.1:7000/docs