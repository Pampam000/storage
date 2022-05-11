import uvicorn
from fastapi import FastAPI
from database import tables
from database.database import engine
from router import router
tables.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run('main:app', host='127.0.0.1', port=8082, reload=True)
