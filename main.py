from fastapi import FastAPI

app = FastAPI()

#https://fastapi.tiangolo.com/async/#in-a-hurry describes when to use async vs normal definitions
@app.get('/')
async def root():
    return {'message': 'Hello World'}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    return {"item_id": item_id}