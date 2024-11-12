'''Цель: научиться описывать и использовать Pydantic модель.

Задача "Модель пользователя":
Подготовка:
Используйте CRUD запросы из предыдущей задачи.
Создайте пустой список users = []
Создайте класс(модель) User, наследованный от BaseModel, который будет содержать следующие поля:
id - номер пользователя (int)
username - имя пользователя (str)
age - возраст пользователя (int)'''
from fastapi import FastAPI, Path, Body, HTTPException
from typing import Annotated
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

'''Измените и дополните ранее описанные 4 CRUD запроса:
get запрос по маршруту '/users' теперь возвращает список users.
post запрос по маршруту '/user/{username}/{age}', теперь:
Добавляет в список users объект User.
id этого объекта будет на 1 больше, чем у последнего в списке users. Если список users пустой, то 1.
Все остальные параметры объекта User - переданные в функцию username и age соответственно.
В конце возвращает созданного пользователя.
put запрос по маршруту '/user/{user_id}/{username}/{age}' теперь:
Обновляет username и age пользователя, если пользователь с таким user_id есть в списке users и возвращает его.
В случае отсутствия пользователя выбрасывается исключение HTTPException с описанием "User was not found" и кодом 404.
delete запрос по маршруту '/user/{user_id}', теперь:
Удаляет пользователя, если пользователь с таким user_id есть в списке users и возвращает его.
В случае отсутствия пользователя выбрасывается исключение HTTPException с описанием "User was not found" и кодом 404.'''
@app.get('/users')
async def get_users() -> List[User]:
    return users

@app.post('/user/{username}/{age}')
async def post_user(user: User) -> str:
    user.id = len(users) + 1
    #user.username = username
    #user.age = age
    users.append(user)
    return f'User with id {user.id} is registered.'

@app.put('/user/{user_id}/{username}/{age}')
async def post_user(user_id: Annotated[int, Path(ge=1, le=999, description='Введите user_id (целое число)', example=10)],
                    username: Annotated[str, Path(min_length=3, max_length=15, description='Введите имя_пользователя', example='UrbanUser')],
                    age: Annotated[int, Path(ge=18, le=120, description='Введите Ваш возраст', example='39')]) -> str:
    try:
        users[user_id].username = username
        users[user_id].age = age
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")
    return f'The user with user_id {user_id} is updated.'

@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=1, le=999, description='Введите user_id (целое число)', example=1)]) -> User:
    try:
        return users.pop(user_id)
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

@app.get('/')
async def main() -> str:
    return 'Перейдите на страницу http://127.0.0.1:8000/docs'

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')
    # https://127.0.0.1:8000/docs

'''Выполните каждый из этих запросов по порядку. Ответы должны совпадать:
1. GET '/users'
[]
2. POST '/user/{username}/{age}' # username - UrbanUser, age - 24
3. POST '/user/{username}/{age}' # username - UrbanTest, age - 36
4. POST '/user/{username}/{age}' # username - Admin, age - 42
5. PUT '/user/{user_id}/{username}/{age}' # user_id - 1, username - UrbanProfi, age - 28
6. DELETE '/user/{user_id}' # user_id - 2
7. GET '/users'
8. DELETE '/user/{user_id}' # user_id - 2'''