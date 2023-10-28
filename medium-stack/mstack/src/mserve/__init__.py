import datetime
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def hello_world():
    return {'msg': 'hello.world', 'now': datetime.datetime.now()}
