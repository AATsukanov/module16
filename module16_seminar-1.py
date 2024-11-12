# Python 3.9
# pip install fastapi==0.111.0
# pip install uvicorn==0.32.0 -- сам встанет

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
async def welcome() -> dict:
    return {'message': 'Привет, Mir!'}

@app.get('/main')
async def welcome() -> dict:
    return {'message': 'Main page'}

@app.get('/id')
async def id_paginator(username: str='Alex', age: int=33) -> dict:
    # запрос в виде:
    # http://127.0.0.1:8000/id?username=UserName&age=34
    return {'User': username, 'Age': age}

@app.get('/user/A/B')
async def news() -> dict:
    return {'message': f'Привет, Tester!'}

@app.get('/user/{first_name}/{last_name}')
async def news(first_name: str, last_name: str) -> dict:
    return {'message': f'Привет, {first_name} {last_name}!'}

# Get -- адрес в строке "?переменная1=значение1&переменная2=значение2"...
# Post -- формы - оформить заказ в магазине...
# Put -- обновить...
# Delete -- удалить...


if __name__ == '__main__':
    print('Версия uvicorn ==', uvicorn.__version__)
    uvicorn.run(app, host='127.0.0.1', port=7000, log_level='info')
    #uvicorn.run(app, host='0.0.0.0', port=5000, log_level='info')

'''
или ДЛЯ ЗАПУСКА СЕРВЕРА (у меня не работает):
В консоли из-под (.venv) python3 -m unicorn main:app
или python3 -m uvicorn module16_seminar-1:app
запускается сервер, высвечивается его адрес, например,
http://127.0.0.1:8000
'''