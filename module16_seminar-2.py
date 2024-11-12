from fastapi import FastAPI, Path
from typing import Annotated
import uvicorn

app = FastAPI()

messages_db = {'0': 'First post in FastAPI'}

@app.get('/')
async def get_all_message() -> dict:
    return messages_db

@app.get('/message/{message_id}')
async def get_message(message_id: str) -> str:
    return messages_db[message_id]

@app.post('/message')
async def create_message(message: str) -> str:
    current_index = str(int(max(messages_db, key=int)) + 1)
    messages_db[current_index] = message
    return 'CREATED: Сообщение создано.'

@app.put('/message/{message_id}')
async def update_message(message_id: str, message: str) -> str:
    messages_db[message_id] = message
    return 'UPDATED: Сообщение обновлено.'

@app.delete('/message/{message_id}')
async def delete_message(message_id: str) -> str:
    messages_db.pop(message_id)
    return 'DELETED: Сообщение удалено.'

@app.delete('/')
async def delete_all_messages() -> str:
    messages_db.clear()
    return 'DELETED: Все сообщения удалены.'

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=7000, log_level='info')
    # https://127.0.0.1:7000/docs