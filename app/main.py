import uvicorn

from fastapi import FastAPI
from api.api_v1.routers import auth, forum, answer


app = FastAPI()
app.include_router(auth.router)
app.include_router(forum.router)
app.include_router(answer.router)



@app.get('/')
async def root():
     return {'message': 'Hello my friend!'}



if __name__ == '__main__':
     uvicorn.run('main:app', reload=True)
     

