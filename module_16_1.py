from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
async def main():
    return "Главная страница"

@app.get('/admin')
async def admin():
    return "Вы вошли как администратор"

# /user/007
@app.get('/user/{user_id}')
async def user(user_id):
    return f'Вы вошли как пользователь № {user_id}'

# /user?username=UserName&age=33
@app.get('/user')
async def news(username: str, age: int):
    return f'Информация о пользователе. Имя: {username}, Возраст: {age}'

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')
    # ПОТОМ ЗАЙТИ НА docs: http://127.0.0.1:8000/docs