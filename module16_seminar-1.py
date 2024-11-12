# Python 3.9
# pip install fastapi==0.111.0
# pip install uvicorn==0.32.0 -- сам встанет

from fastapi import FastAPI, Path
import uvicorn

app = FastAPI()

@app.get('/')
async def welcome() -> dict:
    return {'message': 'Привет, Mir!'}

@app.get('/main')
async def main() -> dict:
    return {'message': 'Главная страница'}

@app.get('/id')
async def id_paginator(username: str='Alex', age: int=33) -> dict:
    # запрос в виде:
    # http://127.0.0.1:8000/id?username=UserName&age=34
    return {'User': username, 'Age': age}

@app.get('/user/{username}/{id}')
async def user(username: str=Path(min_length=4, max_length=15, description='Введите username', example='Alex'),
               id: int=Path(ge=0, le=999, description='Введите Ваш id', example='100')) -> dict:
    return {'message': f'Привет, {username} ({id})!'}

# Get -- адрес в строке "?переменная1=значение1&переменная2=значение2"...
# Post -- формы - оформить заказ в магазине...
# Put -- обновить...
# Delete -- удалить...


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=7000, log_level='info')

'''
или ДЛЯ ЗАПУСКА СЕРВЕРА (у меня не работает):
В консоли из-под (.venv) python3 -m uvicorn main:app
или python3 -m uvicorn module16_seminar-1:app
запускается сервер, высвечивается его адрес, например,
http://127.0.0.1:8000
'''