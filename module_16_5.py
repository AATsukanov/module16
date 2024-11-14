'''Цель: научиться взаимодействовать с шаблонами Jinja 2 и использовать их в запросах.

Задача "Список пользователей в шаблоне":
Подготовка:
Используйте код из предыдущей задачи.
Скачайте заготовленные шаблоны для их дополнения.
Шаблоны оставьте в папке templates у себя в проекте.
Создайте объект Jinja2Templates, указав в качестве папки шаблонов - templates.
Измените и дополните ранее описанные CRUD запросы:

Напишите новый запрос по маршруту '/':
Функция по этому запросу должна принимать аргумент request и возвращать TemplateResponse.
TemplateResponse должен подключать ранее заготовленный шаблон 'users.html',
а также передавать в него request и список users.
Ключи в словаре для передачи определите самостоятельно в соответствии с шаблоном.

Измените get запрос по маршруту '/user' на '/user/{user_id}':
Функция по этому запросу теперь принимает аргумент request и user_id.
Вместо возврата объекта модели User, теперь возвращается объект TemplateResponse.
TemplateResponse должен подключать ранее заготовленный шаблон 'users.html',
а также передавать в него request и одного из пользователей - user.
Ключи в словаре для передачи определите самостоятельно в соответствии с шаблоном.
Создайте несколько пользователей при помощи post запроса со следующими данными:
username - UrbanUser, age - 24
username - UrbanTest, age - 22
username - Capybara, age - 60
В шаблоне 'users.html' заготовлены все необходимые теги и обработка условий,
вам остаётся только дополнить закомментированные строки вашим Jinja 2 кодом
(использование полей id, username и age объектов модели User):
1. По маршруту '/' должен отображаться шаблон 'users.html' со списком всех ранее созданных объектов:
...
2. Здесь каждая из записей является ссылкой на описание объекта,
информация о котором отображается по маршруту '/user/{user_id}': ...
'''
from fastapi import FastAPI, Path, HTTPException, Request #, Body
from fastapi.responses import HTMLResponse
from typing import Annotated
from pydantic import BaseModel
#from typing import List
import uvicorn
# pip install Jinja2
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

'''Напишите новый запрос по маршруту '/':
Функция по этому запросу должна принимать аргумент request и возвращать TemplateResponse.
TemplateResponse должен подключать ранее заготовленный шаблон 'users.html',
а также передавать в него request и список users.
Ключи в словаре для передачи определите самостоятельно в соответствии с шаблоном.'''
@app.get("/")
def get_all_messages(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get('/users/{user_id}')
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail=f"Пользователь с id={user_id} не найден")

@app.post('/user/{username}/{age}')
async def post_user(user: User) -> str:
    if users:
        user.id = max(users, key=lambda usr: usr.id).id + 1
    else:
        user.id = 1
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

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000, log_level='info')