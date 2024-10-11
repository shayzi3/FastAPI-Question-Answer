import uvicorn

from fastapi import FastAPI

from api.api_v1.routers import (
     admin,
     auth,
     forum,
     answer
)


app = FastAPI()

app.include_router(auth.router_auth)
app.include_router(forum.router_forum)
app.include_router(answer.router_answer)
app.include_router(admin.router_admin)



@app.get('/')
async def root():
     return {'message': 'Hello my friend!'}



if __name__ == '__main__':
     uvicorn.run('main:app', reload=True)
     

